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

import plotly.graph_objects as go

st.set_page_config(page_title="Dagilim Grafikleri", layout="wide")

if 'swap_axes' not in st.session_state:
    st.session_state.swap_axes = False

st.title("Oyuncu Dağılım Grafiği")
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
df, top5 = scatterplot.filter_data(selected_league, selected_season, selected_position, min_minutes_played)
# Add multiselect for custom players to be annotated
custom_players = st.sidebar.multiselect("Oyuncuları göster:", df['Oyuncu'].unique())

# Button to reverse X and Y axis variables
if st.sidebar.button("Değişkenleri Ters Çevir"):
    st.session_state.swap_axes = not st.session_state.swap_axes
# Swap variables based on session state
if st.session_state.swap_axes:
    xx, yy = yy, xx

df_sorted = df.sort_values(by=[xx, yy], ascending=[False, False]).head(10)

# Add a new column to identify custom selected players and top 10 players
df['annotation'] = df['Oyuncu'].apply(lambda x: 'Custom' if x in custom_players else ('Top10' if x in df_sorted['Oyuncu'].values else ''))

# Create scatterplot
fig = px.scatter(
    data_frame=df,
    x=xx,
    y=yy,
    color=point_color,
    color_continuous_scale=point_colorscale,
    text=df.apply(lambda row: (
        '' if row['Oyuncu'] in custom_players else 
        (row['Oyuncu'] if row['Oyuncu'] in df_sorted['Oyuncu'].values else '')), axis=1),
    hover_data=['Kulüp', 'Yaş', 'Ana Pozisyon', 'Oynadığı dakikalar'],
    hover_name="Oyuncu",
    title=f"<b>{selected_league} - {selected_season} - {selected_position} Oyuncu Dağılımı</b>",
    width=900,
    height=700
)

# Add custom players annotations with bold text and red color
for player in custom_players:
    player_data = df[df['Oyuncu'] == player]
    fig.add_trace(go.Scatter(
        x=player_data[xx],
        y=player_data[yy],
        mode="markers+text",
        name=player,
        text=f"<b>{player_data['Oyuncu'].iloc[0]}</b>",
        textposition="top right",
        textfont=dict(
            size=14,
            color="#FF0400"
        ),
        marker=dict(size=10, color='green', line=dict(width=1, color='black')),
        hoverinfo='text',
        hovertext=player_data.apply(lambda row: (
            f"<b>{row['Oyuncu']}</b><br><br>"
            f"{xx}= {row[xx]}<br>"
            f"{yy}= {row[yy]}<br>"
            f"Kulüp= {row['Kulüp']}<br>"
            f"Yaş= {row['Yaş']}<br>"
            f"Ana Pozisyon= {row['Ana Pozisyon']}<br>"
            f"Oynadığı dakikalar= {row['Oynadığı dakikalar']}<br>"
        ), axis=1)
    ))

fig.update_traces(textposition='top right', marker=dict(size=10))
fig.update_layout(
    height=700, 
    width=900,
    xaxis_title=f"<b>{xx}</b>",
    yaxis_title=f"<b>{yy}</b>",
    coloraxis_colorbar=dict(orientation="h")
)

# Add horizontal and vertical median lines
fig.add_hline(y=df[yy].median(), name='Median', line_width=0.5)
fig.add_vline(x=df[xx].median(), name='Median', line_width=0.5)

# Watermark annotation
fig.update_layout(
    annotations=[
        dict(
            name="draft watermark",
            text="<b>@ALFIESCOUTING</b>",
            textangle=0,
            opacity=1,
            font=dict(color="#FF0400", size=20),
            xref="paper",
            yref="paper",
            x=0.99,
            y=0.005,
            showarrow=False,
        )
    ]
)

# Config for exporting the plot
config = {
  'toImageButtonOptions': {
    'format': 'png',  # one of png, svg, jpeg, webp
    'filename': 'custom_image',
    'height': 700,
    'width': 900,
    'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
  },
  'responsive': False,
  'scrollZoom': False
}

st.plotly_chart(fig, config=config, use_container_width=False, theme=None, height=700, width=900, key="scatter")
