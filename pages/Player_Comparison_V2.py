import streamlit as st
import pandas as pd
from scripts import utils
from scripts.config import get_position_to_schema, get_params_list, get_schema_params, get_label_mapping, get_column_mapping, position_options
from matplotlib.font_manager import FontProperties

st.title("Player Comparison Radar Chart")
st.sidebar.header("Player Selection")

schema_type = st.sidebar.toggle("Kendi şablonumu kullanmak istiyorum")

all_leagues_df = utils.load_top_9_leagues()
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", position_options+["All"])
df = utils.filter_by_position(all_leagues_df, selected_position)
df = df[df['Minutes played'] >= 900]
currentseason = df[df['Season'] == '23-24']

selected_players = st.sidebar.multiselect("Select Players to Compare", df['Player'].unique())

seasons = {}
for player in selected_players:
    seasons[player] = st.sidebar.selectbox(f"Select Season for {player}", df[df['Player'] == player]['Season'].unique())
    
if schema_type:
    st.sidebar.header("Özel Şablon Oluşturma")
    custom_schema_name = st.sidebar.text_input("Özel Şablon Adı")
    available_metrics = get_params_list()

    # Initialize session state for the custom schema
    if "custom_schema" not in st.session_state:
        st.session_state.custom_schema = []

    # Select metrics for the custom schema
    selected_metrics = st.sidebar.multiselect("Şablon için metrikleri seçin", available_metrics)
    st.session_state.custom_schema = selected_metrics

    # Save the custom schema
    if st.sidebar.button("Özel Şablonu Kaydet"):
        if custom_schema_name:
            if "custom_schemas" not in st.session_state:
                st.session_state.custom_schemas = {}
            st.session_state.custom_schemas[custom_schema_name] = st.session_state.custom_schema
            st.sidebar.success(f"Özel şablon '{custom_schema_name}' kaydedildi.", icon="✅")
            st.session_state.custom_schema = []  # Reset custom schema after saving
        else:
            st.sidebar.error("Lütfen şablon adı giriniz.")