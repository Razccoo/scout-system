import streamlit as st
import numpy as np
from scripts import schemas, utils, scatterplot
import warnings
warnings.filterwarnings('ignore')
import plotly.express as px
import plotly.figure_factory as ff
from plotly.graph_objects import Layout
from scipy import stats
from statistics import mean
from math import pi
import matplotlib.pyplot as plt
if 'swap_axes' not in st.session_state:
    st.session_state.swap_axes = False

st.set_page_config(page_title="Dagilim Grafikleri")

st.title("Oyuncu Dağılım Grafiği Programı")
st.subheader("Hazırlayan Alfie (Twitter: @AlfieScouting)")
st.sidebar.header("Seçenekler")

league_list = list(utils.load_lg_data())
params = scatterplot.param_list
params.sort()

selected_league = st.sidebar.selectbox("Lig Seçiniz", league_list, index=(league_list.index("Süper Lig") if "Süper Lig" in league_list else 0))
selected_season = st.sidebar.selectbox("Sezon Seçiniz", utils.load_lg_data(selected_league))
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", schemas.position_options)
min_minutes_played = st.sidebar.number_input("Minimum Oynanan Dakikalar", value=900, min_value=0)
x_axis = st.sidebar.selectbox(f"Yatay (X) Ekseni", params)
y_axis = st.sidebar.selectbox(f"Dikey (Y) Ekseni", params)
point_color = st.sidebar.selectbox("Nokta Renk Değişkeni", params, index=(params.index("Yaş") if "Yaş" in params else 0))

scale_options = scatterplot.colorscale()
point_colorscale = st.sidebar.selectbox("Nokta Renk Skalası", scale_options, index=(scale_options.index("plasma") if "plasma" in scale_options else 0))

xx, yy = x_axis, y_axis

# Button to reverse X and Y axis variables
if st.sidebar.button("Değişkenleri Ters Çevir"):
    st.session_state.swap_axes = not st.session_state.swap_axes
# Swap variables based on session state
if st.session_state.swap_axes:
    xx, yy = yy, xx

df, top5 = scatterplot.filter_data(selected_league, selected_season, selected_position, min_minutes_played)

config = {'responsive': False}
# Create scatterplot
fig = px.scatter(
    df,
    x=xx,
    y=yy,
    color=point_color,
    color_continuous_scale=point_colorscale,
    text = 'Oyuncu',
    hover_data=['Kulüp', 'Yaş', 'Ana Pozisyon', 'Oynadığı dakikalar'],
    hover_name="Oyuncu",
    title=f"{selected_league} - {selected_season} - {selected_position} Oyuncu Dağılımı",
    width=900,
    height=700
)
fig.update_traces(textposition='top right', marker=dict(size=10, line=dict(width=1, color='black')))

fig.add_hline(y=df[yy].median(), name='Median', line_width=0.5)
fig.add_vline(x=df[xx].median(), name='Median', line_width=0.5)

# Update layout
fig.update_layout(
    xaxis_title=xx,
    yaxis_title=yy,
    coloraxis_colorbar=dict(
        title=point_color
    )
)
st.plotly_chart(fig, theme=None, config=config)