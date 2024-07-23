import streamlit as st
import pandas as pd
import numpy as np
from scripts import utils
from scripts.config import get_params_list, get_column_mapping, position_options

st.set_page_config(page_title="Player Rating Model")

st.title("Potential Player Finder")
st.sidebar.header("Options")

# Load Leagues and Seasons
league_list = list(utils.load_lg_data())
selected_leagues = st.sidebar.multiselect("Select Leagues", league_list)
selected_seasons = st.sidebar.multiselect("Select Seasons", utils.load_lg_data(selected_leagues[0]) if selected_leagues else [])

if selected_leagues and selected_seasons:
    data = []
    for league in selected_leagues:
        for season in selected_seasons:
            data.append(utils.load_player_data(league, season))
    df = pd.concat(data)

    # Rename columns for display
    df.rename(columns=get_column_mapping(), inplace=True)
    
    st.subheader("Loaded Data")
    st.write(df.head())
    
    # Define custom rating model
    st.sidebar.header("Rating Model")
    params = get_params_list()
    selected_params = st.sidebar.multiselect("Select Parameters", params)
    
    if selected_params:
        weights = {}
        for param in selected_params:
            weight = st.sidebar.slider(f"Weight for {param}", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
            weights[param] = weight
        
        # Calculate player ratings
        df['Rating'] = df[selected_params].apply(lambda row: sum(row[param] * weights[param] for param in selected_params), axis=1)
        df = df.sort_values(by='Rating', ascending=False)
        
        st.subheader("Filtered Players")
        st.write(df[['Oyuncu', 'Kulüp', 'Rating'] + selected_params].head(10))
