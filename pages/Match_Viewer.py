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
    # Example processing: extract match information
    match_info = {
        "Match ID": data.get('matchId', 'N/A'),
        "Date": data.get('date', 'N/A'),
        "Home Team": data.get('home', {}).get('name', 'N/A'),
        "Away Team": data.get('away', {}).get('name', 'N/A'),
        "Score": f"{data.get('home', {}).get('score', 'N/A')} - {data.get('away', {}).get('score', 'N/A')}",
    }
    
    # Convert to DataFrame for display
    match_info_df = pd.DataFrame.from_dict([match_info])
    return match_info_df

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
    match_info_df = process_match_data(data)
    st.dataframe(match_info_df)

    # Add more sections here for detailed data exploration
    # For example, team stats, player stats, etc.

else:
    st.write('Please select a JSON file to view the match data.')

# Footer
st.write('Developed by Your Name')
