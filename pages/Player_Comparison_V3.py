import streamlit as st
from scripts import utils
from scripts.config import get_column_mapping, position_options

import matplotlib.pyplot as plt
import numpy as np

def generate_radar_chart(player_data, player_names, metrics, radar_high, radar_low):
    """
    Generates a radar chart comparing selected players based on the selected metrics.
    
    :param player_data: List of player stats for each selected player, each as a list of metric values.
    :param player_names: List of player names corresponding to the player data.
    :param metrics: List of metric names to be used in the radar chart.
    :param radar_high: Series or list of high values (95th quantile) for each metric.
    :param radar_low: Series or list of low values (5th quantile) for each metric.
    :return: Matplotlib figure object of the radar chart.
    """
    # Number of variables we're plotting.
    num_vars = len(metrics)

    # Compute angle for each axis in the radar chart
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Complete the loop to connect the last point back to the first
    angles += angles[:1]

    # Create the radar chart figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Plot high and low quantile ranges as reference
    ax.fill(angles, np.concatenate((radar_high, [radar_high[0]])), color='red', alpha=0.1, label='95th Quantile')
    ax.fill(angles, np.concatenate((radar_low, [radar_low[0]])), color='blue', alpha=0.1, label='5th Quantile')

    # Plot each player's data
    for player_stats, player_name in zip(player_data, player_names):
        # Normalize player stats to the 0-1 range between radar_low and radar_high
        normalized_stats = (player_stats - radar_low) / (radar_high - radar_low)
        normalized_stats = np.clip(normalized_stats, 0, 1)  # Clip to avoid out-of-bounds issues
        values = normalized_stats.tolist() + [normalized_stats[0]]  # Repeat the first value to close the loop

        ax.plot(angles, values, linewidth=2, linestyle='solid', label=player_name)
        ax.fill(angles, values, alpha=0.25)

    # Set the labels for each metric on the radar chart
    ax.set_yticklabels([])  # Remove radial axis labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    # Set chart title and grid options
    ax.set_title("Player Comparison Radar Chart", size=20, pad=20)
    ax.grid(True)

    return fig

######################################################################################################
######################################################################################################

# Title
st.title("Player Comparison Radar Chart")

# Sidebar Header
st.sidebar.header("Player Selection")

# Load data
leagues_df = utils.load_top_9_leagues()

# Define available metrics for schema
available_metrics = get_column_mapping().keys()

# Custom Schema Toggle
create_custom_schema = st.sidebar.checkbox("Create Custom Schema")

# Initialize session state for custom schemas if not already present
if 'custom_schemas' not in st.session_state:
    st.session_state.custom_schemas = {}

if create_custom_schema:
    # Custom Schema Name
    schema_name = st.sidebar.text_input("Enter Schema Name")
    
    # Metric Selection for Custom Schema
    selected_metrics = st.sidebar.multiselect("Select Metrics for Schema", available_metrics)

    # Save Custom Schema
    if st.sidebar.button("Save Schema") and schema_name and selected_metrics:
        st.session_state.custom_schemas[schema_name] = selected_metrics
        st.sidebar.success(f"Schema '{schema_name}' saved.")

# Schema Selection
schema_options = ["Default Schema"] + list(st.session_state.custom_schemas.keys())
selected_schema = st.sidebar.selectbox("Select Schema", schema_options)

# Retrieve selected metrics based on selected schema
if selected_schema == "Default Schema":
    selected_metrics = available_metrics  # or a default set of metrics
else:
    selected_metrics = st.session_state.custom_schemas[selected_schema]
    
######################################################################################################
######################################################################################################

selected_position = st.sidebar.selectbox("Select Position", position_options + ["All"])

# Filter DataFrame based on selected position
df = utils.filter_by_position(leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]  # Filter for players with 900+ minutes played

# Player Selection
selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

######################################################################################################
######################################################################################################

# Define available seasons
available_seasons = df['Season'].unique()

# Season selection for each player
player_seasons = {}
for player in selected_players:
    season = st.sidebar.selectbox(f"Select Season for {player}", available_seasons)
    player_seasons[player] = season

######################################################################################################
######################################################################################################

# Filter original dataframe for 23-24 season to determine radar chart ranges
reference_df = leagues_df[leagues_df['Season'] == '23-24']
radar_high = reference_df[selected_metrics].quantile(0.95)
radar_low = reference_df[selected_metrics].quantile(0.05)

# Generate radar chart for selected players
if selected_players:
    # Fetch data for each player based on selected season
    player_data = []
    for player in selected_players:
        season = player_seasons[player]
        player_stats = df[(df['Player'] == player) & (df['Season'] == season)][selected_metrics]
        if not player_stats.empty:
            player_data.append(player_stats.iloc[0].values)

    # Draw Radar Chart
    if player_data:
        fig = generate_radar_chart(player_data, selected_players, selected_metrics, radar_high, radar_low)
        st.pyplot(fig)