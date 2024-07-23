import streamlit as st
import pandas as pd
import numpy as np
from scripts import utils
from scripts.config import get_params_list, get_column_mapping, get_schema_params, position_options

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
    schema = get_schema_params()
    selected_categories = st.sidebar.multiselect("Select Categories", list(schema.keys()))
    
    if selected_categories:
        category_weights = {}
        parameter_weights = {}
        for category in selected_categories:
            category_weight = st.sidebar.slider(f"Weight for {category}", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
            category_weights[category] = category_weight
            
            params = schema[category]
            selected_params = st.sidebar.multiselect(f"Select Parameters for {category}", params)
            if selected_params:
                parameter_weights[category] = {}
                for param in selected_params:
                    weight = st.sidebar.slider(f"Weight for {param} in {category}", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
                    parameter_weights[category][param] = weight
        
        # Calculate z-scores and player ratings
        df_zscore = df.copy()
        for category, params in parameter_weights.items():
            for param in params:
                df_zscore[param] = (df_zscore[param] - df_zscore[param].mean()) / df_zscore[param].std()
        
        df['Rating'] = df_zscore.apply(lambda row: sum(row[param] * parameter_weights[category][param] * category_weights[category] for category in parameter_weights for param in parameter_weights[category]), axis=1)
        
        # Scale ratings to 100
        df['Rating'] = (df['Rating'] - df['Rating'].min()) / (df['Rating'].max() - df['Rating'].min()) * 100
        df = df.sort_values(by='Rating', ascending=False)
        
        st.subheader("Filtered Players")
        st.write(df[['Oyuncu', 'Kulüp', 'Rating'] + [param for category in parameter_weights for param in parameter_weights[category]]].head(10))
