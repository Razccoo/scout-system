import streamlit as st
import pandas as pd
from scripts import utils
from scripts.config import get_position_to_schema, get_params_list, get_schema_params, get_label_mapping, get_column_mapping, position_options
from matplotlib.font_manager import FontProperties

st.title("Player Comparison Radar Chart")
st.sidebar.header("Player Selection")

schema_type = st.sidebar.toggle("Kendi şablonumu kullanmak istiyorum")

all_leagues_df = utils.load_top_9_leagues()
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", position_options+["All"])
df = utils.filter_by_position(all_leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]
currentseason = df[df['Season'] == '23-24']

selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

if schema_type:
    st.sidebar.header("Özel Şablon Oluşturma")
    custom_schema_name = st.sidebar.text_input("Özel Şablon Adı")
    num_groups = st.sidebar.number_input("Grup Sayısı", min_value=1, max_value=10, value=1)
    available_metrics = get_params_list()
    custom_schema = {}

    for i in range(1, num_groups + 1):
        selected_metrics = st.sidebar.multiselect(f"Grup {i} için metrikleri seçin", available_metrics)
        custom_schema[f"Group {i}"] = selected_metrics
    
    if st.sidebar.button("Özel Şablonu Kaydet"):
        if "custom_schemas" not in st.session_state:
            st.session_state.custom_schemas = {}
        st.session_state.custom_schemas[custom_schema_name] = custom_schema
        st.sidebar.success(f"Özel şablon '{custom_schema_name}' kaydedildi.", icon="✅")

if schema_type:
    schema_options = ["Default Schema"] + list(get_schema_params().keys())
    if "custom_schemas" in st.session_state:
        schema_options += list(st.session_state.custom_schemas.keys())
    selected_schema = st.sidebar.selectbox("Şablon Seçin", schema_options)
else:
    schema_options = ["Default Schema"] + list(get_schema_params().keys())
    selected_schema = st.sidebar.selectbox("Şablon Seçin", schema_options)
            
# schema_options = ["Default Schema"] + list(get_schema_params().keys())
# selected_schema = st.sidebar.selectbox("Şablon Seçin", schema_options)

seasons = {}
for player in selected_players:
    seasons[player] = st.sidebar.selectbox(f"Select Season for {player}", df[df['Player'] == player]['Season'].unique())

if st.sidebar.button("Generate Radar Chart"):
    players_data = []
    for player, season in seasons.items():
        player_data = df[(df['Player'] == player) & (df['Season'] == season)]
        players_data.append(player_data)

    combined_df = pd.concat(players_data)
    player_main_position = combined_df.loc[combined_df['Player'] == selected_players[0], 'Main Position'].values[0]

    selected_schema_type = get_position_to_schema().get(player_main_position)
    schema = get_schema_params()
    label_mapping = get_label_mapping()
    column_mapping = get_column_mapping()

    new_schema = {category: {subcategory: [label_mapping.get(column_mapping.get(param, param), param) for param in params]
                             for subcategory, params in params_dict.items()}
                  for category, params_dict in schema.items()}

    if selected_schema == "Default Schema":
        schema_to_use = new_schema[selected_schema_type]
    elif selected_schema not in ["Default Schema"] + list(get_schema_params().keys()):
        schema_to_use = selected_schema
    else:
        schema_to_use = new_schema[selected_schema]

    original_params = []
    for group in schema[selected_schema_type if selected_schema == "Default Schema" else selected_schema].values():
        original_params.extend(group)

    params = []
    for group in schema_to_use.values():
        params.extend(group)

    cols = ['Player', 'Team within selected timeframe', 'Season'] + original_params

    currentseason = currentseason[cols].rename(columns=column_mapping).rename(columns=label_mapping)
    combined_df = combined_df[cols].rename(columns=column_mapping).rename(columns=label_mapping)

    low = currentseason[params].quantile(0.05).tolist()
    high = currentseason[params].quantile(0.95).tolist()

    utils.player_comparison_radar(combined_df, selected_players, params, low, high)