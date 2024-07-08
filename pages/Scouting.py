import streamlit as st
import pandas as pd
import numpy as np
from scripts import schemas, utils

st.set_page_config(page_title="Talent Finder", page_icon="📈")

st.title("Football Talent Finder")
st.subheader("Tüm veriler Wyscout'tan")
st.subheader('Hazırlayan @AlfieScouting')
st.sidebar.header("Seçenekler")

@st.cache_data
def load_data():
    data = utils.load_all_csv_files()
    return data

data = load_data()
st.write(pd.DataFrame(data))