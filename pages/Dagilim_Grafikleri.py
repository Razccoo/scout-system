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
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
from highlight_text import fig_text, ax_text
from adjustText import adjust_text
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib import cm

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
df, top5 = scatterplot.filter_data(selected_league, selected_season, selected_position, min_minutes_played)
# Add multiselect for custom players to be annotated
custom_players = st.sidebar.multiselect("Oyuncuları göster:", df['Oyuncu'].unique())

# Button to reverse X and Y axis variables
if st.sidebar.button("Eksenleri Ters Çevir"):
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
    'filename': f'{xx}-{yy}-{selected_position}-{selected_league}-{selected_season}',
    'height': 700,
    'width': 900,
    'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
  },
  'responsive': False,
  'scrollZoom': False
}

st.plotly_chart(fig, config=config, use_container_width=False, theme=None, height=700, width=900, key="scatter")

################################################################################################################
################################################################################################################

fig = plt.figure(figsize=(8,8), dpi=100)
ax = plt.subplot()
ax.grid(visible=True, ls='--', color='lightgrey')

ax.scatter(
    df_plot['per_90'], df_plot['succ_rate'], 
    c=df_plot['zscore'], cmap='inferno', 
    zorder=3, ec='grey', s=55, alpha=0.8)
    
texts = []
annotated_df = df_plot[df_plot['annotated']].reset_index(drop=True)
for index in range(annotated_df.shape[0]):
    texts += [
        ax.text(
            x=annotated_df['per_90'].iloc[index], y=annotated_df['succ_rate'].iloc[index],
            s=f"{annotated_df['player_first_name'].iloc[index][0]}. {annotated_df['player_last_name'].iloc[index]}",
            path_effects=[path_effects.Stroke(linewidth=2, foreground=fig.get_facecolor()), 
            path_effects.Normal()], color='black',
            family='DM Sans', weight='bold'
        )
    ]

adjust_text(texts, only_move={'points':'y', 'text':'xy', 'objects':'xy'})

ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(.1))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0%}'))
ax.set_xlim(0)
ax.set_ylim(0,1)

ax.set_ylabel('Long ball success rate (%)')
ax.set_xlabel('Long balls per 90')

fig_text(
    x = 0.09, y = .99, 
    s = "The Premier League's Quarter Backs",
    va = "bottom", ha = "left",
    fontsize = 20, color = "black", font = "DM Sans", weight = "bold"
)

fig_text(
    x = 0.09, y = 0.91, 
    s = "Long balls per 90 and success rate.\nOnly players with above median minutes & median total long balls are shown.\nViz by @sonofacorner | Season 2022/2023",
    va = "bottom", ha = "left",
    fontsize = 12, color = "#5A5A5A", font = "Karla"
)

plt.savefig(
	"figures/11072022_long_balls.png",
	dpi = 600,
	facecolor = "#EFE9E6",
	bbox_inches="tight",
    edgecolor="none",
	transparent = False
)

plt.savefig(
	"figures/11072022_long_balls_tr.png",
	dpi = 600,
	facecolor = "none",
	bbox_inches="tight",
    edgecolor="none",
	transparent = True
)