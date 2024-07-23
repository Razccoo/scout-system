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
    
    category_count = st.sidebar.number_input("Number of Categories", min_value=1, max_value=10, value=1, step=1)
    categories = {}
    category_weights = []
    
    for i in range(category_count):
        st.sidebar.subheader(f"Category {i+1}")
        category_name = st.sidebar.text_input(f"Category {i+1} Name")
        category_weight = st.sidebar.slider(f"Weight for {category_name}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        category_weights.append(category_weight)
        selected_params = st.sidebar.multiselect(f"Select Parameters for {category_name}", params)
        
        if selected_params:
            param_weights = []
            param_weight_dict = {}
            for param in selected_params:
                weight = st.sidebar.slider(f"Weight for {param} in {category_name}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                param_weights.append(weight)
                param_weight_dict[param] = weight
            
            categories[category_name] = {
                "weight": category_weight,
                "params": param_weight_dict,
                "param_weights": param_weights
            }
    
    if st.sidebar.button("Calculate Ratings"):
        if np.isclose(sum(category_weights), 1.0) and all(np.isclose(sum(values["param_weights"]), 1.0) for values in categories.values()):
            # Calculate z-scores and player ratings
            df_zscore = df.copy()
            for category, values in categories.items():
                for param in values["params"]:
                    df_zscore[param] = (df_zscore[param] - df_zscore[param].mean()) / df_zscore[param].std()
            
            df['Rating'] = df_zscore.apply(lambda row: sum(row[param] * values["params"][param] * values["weight"] for category, values in categories.items() for param in values["params"]), axis=1)
            
            # Scale ratings to 100
            df['Rating'] = (df['Rating'] - df['Rating'].min()) / (df['Rating'].max() - df['Rating'].min()) * 100
            df = df.sort_values(by='Rating', ascending=False)
            
            st.subheader("Filtered Players")
            st.write(df[['Oyuncu', 'Kulüp', 'Rating'] + [param for category in categories for param in categories[category]["params"]]].head(10))
        else:
            st.sidebar.error("The weights for all categories and all parameters in each category must sum up to 1.")
