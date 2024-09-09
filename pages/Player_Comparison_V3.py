import streamlit as st
from scripts import utils
from scripts.config import get_column_mapping, position_options

import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Radar

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

def generate_mplsoccer_radar_chart(player_data, player_names, player_teams, metrics, radar_high, radar_low):
    """
    Generates a radar chart comparing selected players using mplsoccer's Radar class with draw_radar_solid
    and markers for each metric point using ax.scatter. Displays player names and their teams.

    :param player_data: List of player stats for each selected player, each as a list of metric values.
    :param player_names: List of player names corresponding to the player data.
    :param player_teams: List of team names corresponding to each player.
    :param metrics: List of metric names to be used in the radar chart.
    :param radar_high: Series or list of high values (95th quantile) for each metric.
    :param radar_low: Series or list of low values (5th quantile) for each metric.
    :return: Matplotlib figure object of the radar chart.
    """
    # Convert radar_high and radar_low to lists
    min_range = radar_low.tolist()
    max_range = radar_high.tolist()

    # Initialize the Radar object
    radar = Radar(
        params=metrics,  # List of parameter names
        min_range=min_range,  # Minimum range for each parameter
        max_range=max_range,  # Maximum range for each parameter
        num_rings=6,  # Number of concentric circles
        ring_width=1,  # Width of each ring
        center_circle_radius=1  # Radius of the center circle
    )

    # Create the radar figure and axis
    fig, ax = radar.setup_axis(figsize=(8, 8))

    # Draw concentric circles for the radar chart
    radar.draw_circles(ax=ax, facecolor='#f0f0f0', edgecolor='#d9d9d9')

    # Define a list of colors to use for different players
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    # Plot each player's radar using draw_radar_solid with markers
    for idx, (player_stats, player_name, player_team) in enumerate(zip(player_data, player_names, player_teams)):
        # Select a color for the player from the colors list, cycling if more players than colors
        color = colors[idx % len(colors)]

        # Draw radar chart with player's data without clipping to the rings
        radar_poly, vertices = radar.draw_radar_solid(
            values=player_stats.tolist(),
            ax=ax,
            kwargs={'facecolor': color, 'alpha': 0.5, 'edgecolor': color, 'lw': 2}  # Unique color for each player
        )

        # Add 'o' markers for each metric point using scatter
        ax.scatter(vertices[:, 0], vertices[:, 1],
                   c=color, marker='o', s=50, zorder=2)

        # Alternate player name placement between left and right
        if idx % 2 == 0:  # Even index - place on the left
            ax.text(0.1, 1.1 - (idx // 2) * 0.1, player_name, ha='right', va='center', transform=ax.transAxes,
                    fontsize=12, weight='bold', color=color)
            ax.text(0.1, 1.07 - (idx // 2) * 0.1, player_team, ha='right', va='center', transform=ax.transAxes,
                    fontsize=10, color=color)
        else:  # Odd index - place on the right
            ax.text(0.9, 1.1 - ((idx - 1) // 2) * 0.1, player_name, ha='left', va='center', transform=ax.transAxes,
                    fontsize=12, weight='bold', color=color)
            ax.text(0.9, 1.07 - ((idx - 1) // 2) * 0.1, player_team, ha='left', va='center', transform=ax.transAxes,
                    fontsize=10, color=color)

    # Draw the parameter labels and range labels
    radar.draw_param_labels(ax=ax, wrap=15, offset=1)
    radar.draw_range_labels(ax=ax, offset=0.1)

    # # Title and final adjustments
    # ax.set_title("Player Comparison Radar Chart", size=20, pad=20)

    # Return the figure for rendering
    return fig

# Button to generate the radar chart
if st.sidebar.button("Generate Radar Chart"):
    if selected_players:
        # Reference data for radar high and low quantiles
        reference_df = leagues_df[leagues_df['Season'] == '23-24']
        radar_high = reference_df[selected_metrics].quantile(0.95)
        radar_low = reference_df[selected_metrics].quantile(0.05)

        player_data = []
        player_teams = []

        # Collect player data and team names
        for player in selected_players:
            season = player_seasons[player]
            player_stats = df[(df['Player'] == player) & (df['Season'] == season)][selected_metrics]
            team_name = df[(df['Player'] == player) & (df['Season'] == season)]['Team within selected timeframe'].iloc[0] if not player_stats.empty else ""

            if not player_stats.empty:
                player_data.append(player_stats.iloc[0].values)
                player_teams.append(team_name)

        if player_data:
            # Pass player data, names, and team names to the radar chart function
            fig = generate_mplsoccer_radar_chart(player_data, selected_players, player_teams, selected_metrics, radar_high, radar_low)
            st.pyplot(fig)
        else:
            st.warning("No data available for the selected players and seasons.")
    else:
        st.warning("Please select at least one player to generate the radar chart.")