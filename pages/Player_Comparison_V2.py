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

seasons = {}
for player in selected_players:
    seasons[player] = st.sidebar.selectbox(f"Select Season for {player}", df[df['Player'] == player]['Season'].unique())
    
if schema_type:
    st.sidebar.header("Özel Şablon Oluşturma")
    custom_schema_name = st.sidebar.text_input("Özel Şablon Adı")
    available_metrics = get_params_list()

    # Initialize session state for the custom schema
    if "custom_schema" not in st.session_state:
        st.session_state.custom_schema = []

    # Select metrics for the custom schema
    selected_metrics = st.sidebar.multiselect("Şablon için metrikleri seçin", available_metrics)
    st.session_state.custom_schema = selected_metrics

    # Save the custom schema
    if st.sidebar.button("Özel Şablonu Kaydet"):
        if custom_schema_name:
            if "custom_schemas" not in st.session_state:
                st.session_state.custom_schemas = {}
            st.session_state.custom_schemas[custom_schema_name] = st.session_state.custom_schema
            st.sidebar.success(f"Özel şablon '{custom_schema_name}' kaydedildi.", icon="✅")
            st.session_state.custom_schema = []  # Reset custom schema after saving
        else:
            st.sidebar.error("Lütfen şablon adı giriniz.")

builtin_schemas = ["Default Schema"] + list(get_schema_params().keys())

if schema_type:
    schema_options = builtin_schemas
    if "custom_schemas" in st.session_state:
        schema_options += list(st.session_state.custom_schemas.keys())
    selected_schema = st.sidebar.selectbox("Şablon Seçin", schema_options)
else:
    schema_options = builtin_schemas
    selected_schema = st.sidebar.selectbox("Şablon Seçin", schema_options)
    

if st.sidebar.button("Generate Radar Chart"):
    players_data = []
    for player, season in seasons.items():
        player_data = df[(df['Player'] == player) & (df['Season'] == season)]
        players_data.append(player_data)

    combined_df = pd.concat(players_data)
    player_main_position = combined_df.loc[combined_df['Player'] == selected_players[0], 'Main Position'].values[0]

    # Determine schema based on selected option
    schema = get_schema_params() if selected_schema == builtin_schemas else st.session_state.custom_schemas.get(selected_schema, {})
    label_mapping = get_label_mapping()
    column_mapping = get_column_mapping()

    # Map parameters to labels
    params = [label_mapping.get(column_mapping.get(param, param), param) for param in schema]

    # Prepare data columns
    cols = ['Player', 'Team within selected timeframe', 'Season'] + schema

    # Rename columns based on mapping
    currentseason = currentseason[cols].rename(columns=column_mapping).rename(columns=label_mapping)
    combined_df = combined_df[cols].rename(columns=column_mapping).rename(columns=label_mapping)

    # Set low and high percentiles for scaling
    low = currentseason[params].quantile(0.05).tolist()
    high = currentseason[params].quantile(0.95).tolist()

    # Generate radar chart
    utils.player_comparison_radar(combined_df, selected_players, params, low, high)