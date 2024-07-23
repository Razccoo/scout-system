import streamlit as st
import pandas as pd
from scripts import utils
from scripts.config import get_position_to_schema, get_params_list, get_schema_params, get_label_mapping, get_column_mapping, position_options
from matplotlib.font_manager import FontProperties

st.title("Player Comparison Radar Chart")
st.sidebar.header("Player Selection")

<<<<<<< HEAD
=======
base_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/'
league_info_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv'

# Load and filter data
>>>>>>> f7936bcfe89ce73a33f6fc883c72850574130c2d
all_leagues_df = utils.load_top_9_leagues()
<<<<<<< HEAD
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", position_options)
=======
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", schemas.position_options)
>>>>>>> f7936bcfe89ce73a33f6fc883c72850574130c2d
df = utils.filter_by_position(all_leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]
currentseason = df[df['Season'] == '23-24']

selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

schema_options = ["Default Schema"] + list(get_schema_params().keys())
selected_schema = st.sidebar.selectbox("Şablon Seçin", schema_options)

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