import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from scripts import utils
from scripts.config import get_params_list, get_column_mapping, position_options

st.set_page_config(page_title="Player Rating Model")

# Add custom CSS to hide the GitHub icon
hide_github_icon = """
#MainMenu {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

st.title("Potential Player Finder")
st.sidebar.header("Options")

# GitHub directory for templates
templates_dir = "templates"
templates_url = "https://github.com/Razccoo/scout-system/tree/Testing/templates"

# Function to save template
def save_template(template_name, categories):
    template = {"categories": categories}
    file_path = os.path.join(templates_dir, f"{template_name}.json")
    os.makedirs(templates_dir, exist_ok=True)
    with open(file_path, "w") as file:
        json.dump(template, file)
    st.sidebar.success(f"Template '{template_name}' saved successfully.")

# Function to load available templates
def load_templates():
    templates = []
    if os.path.exists(templates_dir):
        for file_name in os.listdir(templates_dir):
            if file_name.endswith(".json"):
                templates.append(file_name[:-5])  # Remove .json extension
    return templates

# Function to load a template
def load_template(template_name):
    file_path = os.path.join(templates_dir, f"{template_name}.json")
    with open(file_path, "r") as file:
        template = json.load(file)
    return template["categories"]

# Initialize session state for categories
if "categories" not in st.session_state:
    st.session_state.categories = {}
if "new_category_name" not in st.session_state:
    st.session_state.new_category_name = ""
if "new_category_weight" not in st.session_state:
    st.session_state.new_category_weight = 0.5
if "new_params" not in st.session_state:
    st.session_state.new_params = []

# Load Leagues and Seasons
league_list = list(utils.load_lg_data())
selected_leagues = st.sidebar.multiselect("Select Leagues", league_list)
selected_seasons = st.sidebar.multiselect("Select Seasons", utils.load_lg_data(selected_leagues[0]) if selected_leagues else [])

# Filter for Minimum Minutes Played
min_minutes_played = st.sidebar.number_input("Minimum Minutes Played", min_value=0, value=900, step=100)

if selected_leagues and selected_seasons:
    data = []
    for league in selected_leagues:
        for season in selected_seasons:
            data.append(utils.load_player_data(league, season))
    df = pd.concat(data)

    # Filter by minimum minutes played
    df = df[df['Minutes played'] >= min_minutes_played]

    # Rename columns for display
    df.rename(columns=get_column_mapping(), inplace=True)
    
    st.subheader("Loaded Data")
    st.write(df.head())
    
    # Define custom rating model
    st.sidebar.header("Rating Model")
    params = get_params_list()
    
    # Option to load a template
    template_option = st.sidebar.selectbox("Load Template", ["None"] + load_templates())
    if template_option != "None":
        st.session_state.categories = load_template(template_option)
        st.sidebar.success(f"Template '{template_option}' loaded successfully.")
    else:
        categories = st.session_state.categories

    # Display and update categories from the loaded template
    if st.session_state.categories:
        category_weights = []
        for category_name, category_info in st.session_state.categories.items():
            st.sidebar.subheader(f"{category_name}")
            category_info["weight"] = st.sidebar.slider(f"Weight for {category_name}", min_value=0.0, max_value=1.0, value=category_info["weight"], step=0.01)
            category_weights.append(category_info["weight"])
            for param in category_info["params"]:
                category_info["params"][param] = st.sidebar.slider(f"Weight for {param} in {category_name}", min_value=0.0, max_value=1.0, value=category_info["params"][param], step=0.01)

    # Add new categories or parameters
    st.sidebar.subheader("Add New Category")
    new_category_name = st.sidebar.text_input("New Category Name")
    new_category_weight = st.sidebar.slider("Weight for New Category", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    new_params = st.sidebar.multiselect("Select Parameters for New Category", params)

    if st.sidebar.button("Add New Category"):
        if new_category_name and new_params:
            param_weight_dict = {}
            param_weights = []
            for param in new_params:
                weight = st.sidebar.slider(f"Weight for {param} in {new_category_name}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                param_weights.append(weight)
                param_weight_dict[param] = weight

            st.session_state.categories[new_category_name] = {
                "weight": new_category_weight,
                "params": param_weight_dict,
                "param_weights": param_weights
            }
            st.experimental_rerun()  # Refresh the sidebar to show the new category

    if st.session_state.categories:
        st.sidebar.subheader("Add New Parameter to Existing Category")
        selected_category = st.sidebar.selectbox("Select Category to Add Parameter", list(st.session_state.categories.keys()))
        new_params = st.sidebar.multiselect(f"Select Parameters for {selected_category}", params)
        
        if st.sidebar.button("Add New Parameter to Existing Category"):
            for param in new_params:
                weight = st.sidebar.slider(f"Weight for {param} in {selected_category}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                st.session_state.categories[selected_category]["params"][param] = weight
                st.session_state.categories[selected_category]["param_weights"].append(weight)
            st.experimental_rerun()  # Refresh the sidebar to show the new parameters

    if st.sidebar.button("Calculate Ratings"):
        category_weights = [category_info["weight"] for category_info in st.session_state.categories.values()]
        if np.isclose(sum(category_weights), 1.0) and all(np.isclose(sum(values["param_weights"]), 1.0) for values in st.session_state.categories.values()):
            # Calculate z-scores and player ratings
            df_zscore = df.copy()
            for category, values in st.session_state.categories.items():
                for param in values["params"]:
                    df_zscore[param] = (df_zscore[param] - df_zscore[param].mean()) / df_zscore[param].std()
            
            # Filter out players with all zero selected parameters
            non_zero_df = df_zscore[df_zscore[[param for values in st.session_state.categories.values() for param in values["params"]]].sum(axis=1) != 0]
            
            non_zero_df['Rating'] = non_zero_df.apply(lambda row: sum(row[param] * values["params"][param] * values["weight"] for category, values in st.session_state.categories.items() for param in values["params"]), axis=1)
            
            # Scale ratings to 100
            non_zero_df['Rating'] = (non_zero_df['Rating'] - non_zero_df['Rating'].min()) / (non_zero_df['Rating'].max() - non_zero_df['Rating'].min()) * 100
            non_zero_df = non_zero_df.sort_values(by='Rating', ascending=False)
            
            st.subheader("Filtered Players")
            st.write(non_zero_df[['Oyuncu', 'Kulüp', 'Rating'] + [param for category in st.session_state.categories for param in st.session_state.categories[category]["params"]]].head(10))
        else:
            st.sidebar.error("The weights for all categories and all parameters in each category must sum up to 1.")
    
    # Option to save the current configuration as a template
    if st.session_state.categories:
        template_name = st.sidebar.text_input("Template Name")
        if st.sidebar.button("Save Template"):
            if template_name:
                save_template(template_name, st.session_state.categories)
            else:
                st.sidebar.error("Please enter a template name.")
