import streamlit as st
import os
import pandas as pd
from socceraction.data.opta import OptaLoader, parsers

# Directory containing the JSON files
root_directory = 'events'

# Function to get subfolders for competition_id
def get_subfolders(directory):
    return [f.name for f in os.scandir(directory) if f.is_dir()]

# Get competition IDs from subfolders under the root directory
competition_ids = get_subfolders(root_directory)

# Sidebar for selecting competition, season, and game
st.sidebar.title('Selection')
selected_competition_id = st.sidebar.selectbox('Competition ID', competition_ids)

# Get season IDs based on the selected competition
if selected_competition_id:
    season_ids = get_subfolders(os.path.join(root_directory, selected_competition_id))
    selected_season_id = st.sidebar.selectbox('Season ID', season_ids)

    # Get game IDs based on the selected season
    if selected_season_id:
        game_ids = get_subfolders(os.path.join(root_directory, selected_competition_id, selected_season_id))
        selected_game_id = st.sidebar.selectbox('Game ID', game_ids)

        # Define the API loader with the selected competition, season, and game
        if selected_game_id:
            api = OptaLoader(
                root=root_directory,
                feeds={"whoscored": f"{selected_competition_id}_{selected_season_id}/{selected_game_id}"},
                parser={"whoscored": parsers.WhoScoredParser}
            )

            # Load and parse data for the selected game
            match_data = api.events(selected_game_id)

            if match_data:
                # match_info = match_data['match']
                # events = match_data['events']

                # # Display match information
                # st.header('Match Information')
                # match_info_df = pd.DataFrame([match_info])
                # st.dataframe(match_info_df)

                # Display event data
                st.header('Match Events')
                # events_df = pd.DataFrame(events)
                st.dataframe(match_data)
            else:
                st.write("No data found for the selected game.")
else:
    st.write("Please select a competition, season, and game.")

# Footer
st.write('Developed by Your Name')
