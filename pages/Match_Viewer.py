import streamlit as st
import pandas as pd
import json
import os

# Directory containing the JSON files
json_directory = 'events/TUR - Super Lig'

# Function to load JSON data
def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

# Function to process JSON data and extract relevant information
def process_match_data(data):
    # Extract basic match information
    match_info = {
        "Match ID": data.get('matchId', 'N/A'),
        "Date": data.get('date', 'N/A'),
        "Home Team": data.get('home', {}).get('name', 'N/A'),
        "Away Team": data.get('away', {}).get('name', 'N/A'),
        "Home Score": data.get('home', {}).get('score', 'N/A'),
        "Away Score": data.get('away', {}).get('score', 'N/A'),
        "Attendance": data.get('attendance', 'N/A'),
    }

    # Convert match info to DataFrame for display
    match_info_df = pd.DataFrame.from_dict([match_info])

    # Extract player statistics for home and away teams
    home_players = data.get('home', {}).get('players', [])
    away_players = data.get('away', {}).get('players', [])

    home_player_stats = []
    for player in home_players:
        player_info = {
            "Name": player.get('name'),
            "Position": player.get('position'),
            "Shirt No": player.get('shirtNo'),
            "Age": player.get('age'),
            "Height": player.get('height'),
            "Weight": player.get('weight'),
            "Is First Eleven": player.get('isFirstEleven'),
            "Is Man of the Match": player.get('isManOfTheMatch')
        }
        home_player_stats.append(player_info)

    away_player_stats = []
    for player in away_players:
        player_info = {
            "Name": player.get('name'),
            "Position": player.get('position'),
            "Shirt No": player.get('shirtNo'),
            "Age": player.get('age'),
            "Height": player.get('height'),
            "Weight": player.get('weight'),
            "Is First Eleven": player.get('isFirstEleven'),
            "Is Man of the Match": player.get('isManOfTheMatch')
        }
        away_player_stats.append(player_info)

    # Convert player stats to DataFrames
    home_player_stats_df = pd.DataFrame(home_player_stats)
    away_player_stats_df = pd.DataFrame(away_player_stats)

    return match_info_df, home_player_stats_df, away_player_stats_df

# App title
st.title('WhoScored Match Data Viewer')

# Sidebar for file selection
st.sidebar.title('File Selection')

# Ensure the directory exists
if os.path.exists(json_directory):
    json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]
else:
    json_files = []

selected_file = st.sidebar.selectbox('Select a JSON file', json_files)

# Load and process the selected JSON file
if selected_file:
    file_path = os.path.join(json_directory, selected_file)
    data = load_json(file_path)
    
    # Display basic match information
    st.header('Match Information')
    match_info_df, home_player_stats_df, away_player_stats_df = process_match_data(data)
    st.dataframe(match_info_df)

    # Display player statistics for home team
    st.header('Home Team Player Statistics')
    st.dataframe(home_player_stats_df)

    # Display player statistics for away team
    st.header('Away Team Player Statistics')
    st.dataframe(away_player_stats_df)

    # Add more sections here for detailed data exploration
    # For example, specific player stats, events, etc.

else:
    st.write('Please select a JSON file to view the match data.')

# Footer
st.write('Developed by Your Name')
