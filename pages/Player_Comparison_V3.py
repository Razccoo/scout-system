import streamlit as st
from scripts import utils
from scripts.config import get_column_mapping, position_options

import matplotlib.pyplot as plt
import numpy as np

# Load the data and required functions
leagues_df = utils.load_top_9_leagues()
available_metrics = get_column_mapping().keys()

# Set up the Streamlit app page
st.title("Player Comparison Radar Chart")
st.sidebar.header("Player Selection")

# Initialize custom schema handling in session state
if 'custom_schemas' not in st.session_state:
    st.session_state.custom_schemas = {}

# Custom Schema Toggle
create_custom_schema = st.sidebar.checkbox("Create Custom Schema")
if create_custom_schema:
    schema_name = st.sidebar.text_input("Enter Schema Name")
    selected_metrics = st.sidebar.multiselect("Select Metrics for Schema", available_metrics)
    if st.sidebar.button("Save Schema") and schema_name and selected_metrics:
        st.session_state.custom_schemas[schema_name] = selected_metrics
        st.sidebar.success(f"Schema '{schema_name}' saved.")

# Schema Selection
schema_options = ["Default Schema"] + list(st.session_state.custom_schemas.keys())
selected_schema = st.sidebar.selectbox("Select Schema", schema_options)

# Retrieve selected metrics based on selected schema
if selected_schema == "Default Schema":
    selected_metrics = available_metrics  # Default to all available metrics
else:
    selected_metrics = st.session_state.custom_schemas[selected_schema]

# Position and Player Filtering
position_options = ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']
selected_position = st.sidebar.selectbox("Select Position", position_options + ["All"])
df = utils.filter_by_position(leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]
selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

# Season Selection for Each Player
available_seasons = df['Season'].unique()
player_seasons = {player: st.sidebar.selectbox(f"Select Season for {player}", available_seasons) for player in selected_players}

# Define the radar chart generation function
def generate_radar_chart(player_data, player_names, metrics, radar_high, radar_low):
    num_vars = len(metrics)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    ax.fill(angles, np.concatenate((radar_high, [radar_high[0]])), color='red', alpha=0.1, label='95th Quantile')
    ax.fill(angles, np.concatenate((radar_low, [radar_low[0]])), color='blue', alpha=0.1, label='5th Quantile')

    for player_stats, player_name in zip(player_data, player_names):
        normalized_stats = (player_stats - radar_low) / (radar_high - radar_low)
        normalized_stats = np.clip(normalized_stats, 0, 1)
        values = normalized_stats.tolist() + [normalized_stats[0]]

        ax.plot(angles, values, linewidth=2, linestyle='solid', label=player_name)
        ax.fill(angles, values, alpha=0.25)

    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    ax.set_title("Player Comparison Radar Chart", size=20, pad=20)
    ax.grid(True)

    return fig

# Button to generate the radar chart
if st.button("Generate Radar Chart"):
    if selected_players:
        reference_df = leagues_df[leagues_df['Season'] == '23-24']
        radar_high = reference_df[selected_metrics].quantile(0.95)
        radar_low = reference_df[selected_metrics].quantile(0.05)

        player_data = []
        for player in selected_players:
            season = player_seasons[player]
            player_stats = df[(df['Player'] == player) & (df['Season'] == season)][selected_metrics]
            if not player_stats.empty:
                player_data.append(player_stats.iloc[0].values)

        if player_data:
            fig = generate_radar_chart(player_data, selected_players, selected_metrics, radar_high, radar_low)
            st.pyplot(fig)
        else:
            st.warning("No data available for the selected players and seasons.")
    else:
        st.warning("Please select at least one player to generate the radar chart.")
