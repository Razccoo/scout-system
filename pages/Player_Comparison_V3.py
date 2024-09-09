import streamlit as st
from scripts import utils
from scripts.config import get_column_mapping, position_options

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Radar, FontManager

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
selected_position = st.sidebar.selectbox("Select Position", position_options + ["All"])
df = utils.filter_by_position(leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]
selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

# Season Selection for Each Player
available_seasons = df['Season'].unique()
player_seasons = {player: st.sidebar.selectbox(f"Select Season for {player}", available_seasons) for player in selected_players}

# Define the radar chart generation function
def generate_mplsoccer_radar_chart(player_data, player_names, metrics, radar_high, radar_low):
    """
    Generates a radar chart comparing selected players using mplsoccer's Radar class.

    :param player_data: List of player stats for each selected player, each as a list of metric values.
    :param player_names: List of player names corresponding to the player data.
    :param metrics: List of metric names to be used in the radar chart.
    :param radar_high: Series or list of high values (95th quantile) for each metric.
    :param radar_low: Series or list of low values (5th quantile) for each metric.
    :return: Matplotlib figure object of the radar chart.
    """

    # Initialize the Radar object with min and max values for each metric
    radar = Radar(label_fontsize=13, range_fontsize=11, 
                  params=metrics, 
                  min_range=radar_low.tolist(), 
                  max_range=radar_high.tolist())

    # Create a figure and axes using mplsoccer
    fig, ax = radar.setup_axis(figsize=(8, 8))

    # Plot each player's data on the radar chart
    for player_stats, player_name in zip(player_data, player_names):
        # Normalize player stats to fit within the min and max range
        normalized_stats = (player_stats - radar_low) / (radar_high - radar_low)
        normalized_stats = np.clip(normalized_stats, 0, 1)  # Ensure stats are within the range
        radar_values = normalized_stats * (radar_high - radar_low) + radar_low
        
        radar_values = radar_values.tolist()  # Convert to list for plotting
        
        # Plot the radar chart for the player
        radar.draw_radar(ax, values=radar_values, 
                         compare_values=None,  # No comparison data
                         compare_kwargs=None,
                         kwargs={'color': 'green', 'alpha': 0.6, 'lw': 2},
                         label=player_name)

    # Title and legend settings
    ax.set_title("Player Comparison Radar Chart", size=20, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    # Return the figure object for further use in Streamlit or other display contexts
    return fig

# Button to generate the radar chart
if st.sidebar.button("Generate Radar Chart"):
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
            fig = generate_mplsoccer_radar_chart(player_data, selected_players, selected_metrics, radar_high, radar_low)
            st.pyplot(fig)
        else:
            st.warning("No data available for the selected players and seasons.")
    else:
        st.warning("Please select at least one player to generate the radar chart.")
