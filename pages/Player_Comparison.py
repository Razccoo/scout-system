import streamlit as st
import pandas as pd
from scripts import utils, schemas
from matplotlib.font_manager import FontProperties

def replace_params_with_labels(schema, columns, labels):
    schema = schemas.schema_params()
    columns = schemas.column_mapping()
    labels = schemas.label_mapping()
    
    new_schema = {}
    
    for category, params_dict in schema.items():
        new_schema[category] = {}
        for subcategory, params in params_dict.items():
            new_schema[category][subcategory] = []
            for param in params:
                if param in columns:
                    intermediate_column = columns[param]
                    if intermediate_column in labels:
                        final_label = labels[intermediate_column]
                        new_schema[category][subcategory].append(final_label)
                    else:
                        new_schema[category][subcategory].append(intermediate_column)
                else:
                    new_schema[category][subcategory].append(param)
    
    return new_schema


st.title("Player Comparison Radar Chart")
st.sidebar.header("Player Selection")

base_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/'
league_info_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv'

# Load and filter data
all_leagues_df = utils.load_top_9_leagues()
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", schemas.position_options)
df = utils.filter_by_position(all_leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]
currentseason = df[df['Season'] == '23-24']

selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

schema_options = ["Default Schema"] + list(schemas.schema_params().keys())
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
    
    # Determine schema based on player's main position
    selected_schema_type = schemas.position_to_schema().get(player_main_position)
    
    # Replace schema parameters with labels
    schema = replace_params_with_labels(schemas.schema_params(), schemas.column_mapping(), schemas.label_mapping())

    # Use selected schema
    if selected_schema == "Default Schema":
        schema_to_use = schema[selected_schema_type]
    else:
        schema_to_use = schema[selected_schema]

    # Get the original params before mapping
    original_params = []
    for group in schemas.schema_params()[selected_schema_type if selected_schema == "Default Schema" else selected_schema].values():
        original_params.extend(group)

    # Use mapped params for display and calculation
    params = []
    for group in schema_to_use.values():
        params.extend(group)

    # Select columns dynamically based on the original params
    cols = ['Player', 'Team within selected timeframe', 'Season'] + original_params
    
    currentseason = currentseason[cols].rename(columns=schemas.column_mapping()).rename(columns=schemas.label_mapping())
    combined_df = combined_df[cols].rename(columns=schemas.column_mapping()).rename(columns=schemas.label_mapping())
    
    low = currentseason[params].quantile(0.05).tolist()
    high = currentseason[params].quantile(0.95).tolist()

    # Debugging prints
    st.write(f"params: {params}")
    st.write(f"low: {low}")
    st.write(f"high: {high}")
    st.write(f"Length of params: {len(params)}")
    st.write(f"Length of low: {len(low)}")
    st.write(f"Length of high: {len(high)}")
    
    utils.player_comparison_radar(combined_df, selected_players, params, low, high)