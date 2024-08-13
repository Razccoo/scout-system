import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Directory containing the JSON files
json_directory = 'events/TUR - Super Lig/2324'

# Function to load JSON data
def load_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

# Function to process JSON data and extract relevant information
def process_match_data(data):
    # Parse and format the match date
    raw_date = data.get('startDate', 'N/A')
    match_date = datetime.strptime(raw_date, '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d') if raw_date != 'N/A' else 'N/A'

    match_info = {
        "Match Date": match_date,
        "Home Team": data.get('home', {}).get('name', 'N/A'),
        "Away Team": data.get('away', {}).get('name', 'N/A'),
        "Half-Time Score": data.get('htScore', 'N/A'),
        "Full-Time Score": data.get('ftScore', 'N/A'),
        "Attendance": data.get('attendance', 'N/A'),
    }

    # Convert match info to DataFrame for display
    match_info_df = pd.DataFrame([match_info])

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
            "Is Man of the Match": player.get('isManOfTheMatch'),
            "Passes Accurate": sum(player.get('stats', {}).get('passesAccurate', {}).values()),
            "Passes Total": sum(player.get('stats', {}).get('passesTotal', {}).values()),
            "Shots On Target": sum(player.get('stats', {}).get('shotsOnTarget', {}).values()),
            "Shots Total": sum(player.get('stats', {}).get('shotsTotal', {}).values()),
            "Tackles Total": sum(player.get('stats', {}).get('tacklesTotal', {}).values()),
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
            "Is Man of the Match": player.get('isManOfTheMatch'),
            "Passes Accurate": sum(player.get('stats', {}).get('passesAccurate', {}).values()),
            "Passes Total": sum(player.get('stats', {}).get('passesTotal', {}).values()),
            "Shots On Target": sum(player.get('stats', {}).get('shotsOnTarget', {}).values()),
            "Shots Total": sum(player.get('stats', {}).get('shotsTotal', {}).values()),
            "Tackles Total": sum(player.get('stats', {}).get('tacklesTotal', {}).values()),
        }
        away_player_stats.append(player_info)

    # Convert player stats to DataFrames
    home_player_stats_df = pd.DataFrame(home_player_stats)
    away_player_stats_df = pd.DataFrame(away_player_stats)

    return match_info_df, home_player_stats_df, away_player_stats_df

# Function to extract and process event data
def extract_event_data(data, game_id):
    events = data.get('events', [])

    event_data = []
    for event in events:
        event_info = {
            "game_id": game_id,
            "event_id": event.get('id', 'N/A'),
            "period_id": event.get('period', {}).get('value', 'N/A'),
            "team_id": event.get('teamId', 'N/A'),
            "team_name": 'Home' if event.get('teamId') == data.get('home', {}).get('teamId') else 'Away',
            "player_id": event.get('playerId', 'N/A'),
            "player_name": event.get('playerName', 'N/A'),
            "type_id": event.get('type', {}).get('value', 'N/A'),
            "timestamp": event.get('minuteInfo', {}).get('minuteString', 'N/A'),
            "minute": event.get('minute', 'N/A'),
            "second": event.get('second', 'N/A'),
            "outcome": event.get('outcomeType', {}).get('displayName', 'N/A'),
            "start_x": event.get('x', 'N/A'),
            "start_y": event.get('y', 'N/A'),
            "end_x": event.get('endX', 'N/A'),
            "end_y": event.get('endY', 'N/A'),
            "qualifiers": [qualifier.get('type', {}).get('displayName') for qualifier in event.get('qualifiers', [])],
            "touch": event.get('isTouch', False),
            "goal": event.get('isGoal', False),
            "shot": event.get('isShot', False),
            "type_name": event.get('type', {}).get('displayName', 'N/A')
        }
        event_data.append(event_info)

    # Convert the list of dictionaries into a DataFrame
    event_df = pd.DataFrame(event_data)
    return event_df

# Streamlit App
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
    game_id = os.path.splitext(selected_file)[0]  # Use filename without extension as game_id
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

    # Extract and display event data
    st.header('Match Events DataFrame')
    event_df = extract_event_data(data, game_id)
    st.dataframe(event_df)

else:
    st.write('Please select a JSON file to view the match data.')

# Footer
st.write('Developed by Your Name')
