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
import plotly.graph_objects as go

st.set_page_config(page_title="Dagilim Grafikleri", layout="wide")

if 'swap_axes' not in st.session_state:
    st.session_state.swap_axes = False

st.title("Oyuncu Dağılım Grafiği")
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

# Add multiselect for custom players to be annotated
custom_players = st.sidebar.multiselect("Ekstra Oyuncuları Seçin", df['Oyuncu'].unique())

df_sorted = df.sort_values(by=[xx, yy], ascending=[False, False]).head(10)

# Add a new column to identify custom selected players
df_custom = df[df["Oyuncu"].isin(custom_players)]
df = df[~df["Oyuncu"].isin(custom_players)]

# Function to determine the text for annotation
def annotate_text(row):
    if row.name in df_sorted.index:
        return row['Oyuncu']
    elif row['Oyuncu'] in custom_players:
        return f"<b>{row['Oyuncu']}</b>"
    else:
        return ''
    
# Create scatterplot
fig = px.scatter(
    data_frame=df,
    x=xx,
    y=yy,
    color=point_color,
    color_continuous_scale=point_colorscale,
    text = df.apply(annotate_text, axis=1),
    hover_data=['Kulüp', 'Yaş', 'Ana Pozisyon', 'Oynadığı dakikalar'],
    hover_name="Oyuncu",
    title=f"{selected_league} - {selected_season} - {selected_position} Oyuncu Dağılımı",
    # width=900,
    # height=700
    )

draft_template = go.layout.Template()
draft_template.layout.annotations = [
    dict(
        name="draft watermark",
        text="@ALFIESCOUTING",
        textangle=0,
        opacity=1,
        font=dict(color="black", size=20),
        xref="paper",
        yref="paper",
        x=0.99,
        y=0.005,
        showarrow=False,
    )
]

config = {
  'toImageButtonOptions': {
    'format': 'png', # one of png, svg, jpeg, webp
    'filename': 'custom_image',
    'height': 700,
    'width': 900,
    'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
  },
  'responsive': False,
  'scrollZoom': False
}

fig.update_traces(textposition='top right', marker=dict(size=10, line=dict(width=1, color='black')))

for player in custom_players:
    fig.add_scatter(
        x=df_custom[df_custom['Oyuncu'] == player][xx],
        y=df_custom[df_custom['Oyuncu'] == player][yy],
        mode='marker+text',
        text=df_custom[df_custom['Oyuncu'] == player]['Oyuncu'],
        textposition='top right',
        marker=dict(size=10, line=dict(width=1, color='red'))
    )
    
fig.add_hline(y=df[yy].median(), name='Median', line_width=0.5)
fig.add_vline(x=df[xx].median(), name='Median', line_width=0.5)

fig.update_layout(height=700, width=900, coloraxis_colorbar=dict(
        orientation="h"
    ), template=draft_template)

st.plotly_chart(fig, config=config, use_container_width=False, theme=None, height=700, width=900, key="scatter")
