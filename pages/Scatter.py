import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
from highlight_text import fig_text, ax_text
from adjustText import adjust_text
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib import cm
import scipy.stats as stats
import streamlit as st
import requests
from scripts import utils, schemas, scatterplot


from mplsoccer import Pitch

from PIL import Image
import urllib
import os

st.set_page_config(page_title="Dagilim Grafikleri")

if 'swap_axes' not in st.session_state:
    st.session_state.swap_axes = False
    
def plot_scatter(df, xx, yy, selected_league, selected_position, selected_season):
    plt.clf()
    df = utils.filter_by_position(df, selected_position)
    df_plot = df[(df['Oynadığı dakikalar'] >= df['Oynadığı dakikalar'].median()) & (df[xx] >= df[xx].median())]

    df_plot['zscore'] = stats.zscore(df_plot[xx]) * 0.6 + stats.zscore(df_plot[yy]) * 0.4
    df_plot['annotated'] = [True if x > df_plot['zscore'].quantile(0.8) else False for x in df_plot['zscore']]

    fig = plt.figure(figsize=(16, 8), dpi=100)
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 2, 1], wspace=0.05)
    ax = plt.subplot(gs[1])
    ax.grid(visible=True, ls='--', color='lightgrey')

    ax.scatter(
        df_plot[xx], df_plot[yy],
        c=df_plot['zscore'], cmap='inferno',
        zorder=3, ec='grey', s=55, alpha=0.8)
    
    # Function to clean up variable names
    def clean_variable_name(name):
        return name.replace(" / 90", "")

    xx_cleaned = clean_variable_name(xx)
    yy_cleaned = clean_variable_name(yy)

    texts = []
    annotated_df = df_plot[df_plot['annotated']].reset_index(drop=True)
    for index in range(annotated_df.shape[0]):
        texts += [
            ax.text(
                x=annotated_df[xx].iloc[index], y=annotated_df[yy].iloc[index],
                s=f"{annotated_df['Oyuncu'].iloc[index]}",
                path_effects=[path_effects.Stroke(linewidth=2, foreground=fig.get_facecolor()), path_effects.Normal()],
                color='black',
                family='DMSans', weight='bold'
            )
        ]

    adjust_text(texts, only_move={'points': 'y', 'text': 'xy', 'objects': 'xy'})

    ax.set_ylabel(f'{yy}')
    ax.set_xlabel(f'{xx}')

    fig_text(
        x=0.33, y=0.99,
        s=f"{selected_league} {selected_position}",
        va="bottom", ha="left",
        fontsize=20, color="black", font="DMSans", weight="bold"
    )

    fig_text(
        x=0.33, y=0.91,
        s=f"{xx_cleaned} ve {yy_cleaned}\nYalnızca ortanca üzerinde süre alan ve {xx_cleaned.lower()} yapan oyuncular gösterilmiştir.\nHazırlayan @alfiescouting | {selected_season} sezonu",
        va="bottom", ha="left",
        fontsize=12, color="#5A5A5A", font="Karla"
    )

    
    # Add the left image
    image_path_left = "/workspaces/scout-system/assets/IMG_5349 2024-07-10 18_37_12.PNG"
    left_img = plt.imread(image_path_left)
    imagebox_left = OffsetImage(left_img, zoom=0.3)
    ab_left = AnnotationBbox(imagebox_left, (0, 0.5), frameon=False, xycoords='axes fraction', boxcoords="axes fraction", box_alignment=(0.5, 0.5))
    ax.add_artist(ab_left)

    # Add the right image
    image_path_right = "/workspaces/scout-system/assets/IMG_5348 2024-07-10 18_37_11.PNG"
    right_img = plt.imread(image_path_right)
    imagebox_right = OffsetImage(right_img, zoom=0.3)
    ab_right = AnnotationBbox(imagebox_right, (1, 0.5), frameon=False, xycoords='axes fraction', boxcoords="axes fraction", box_alignment=(0.5, 0.5))
    ax.add_artist(ab_right)

    return fig
    
    # plt.savefig(
    #     "figures/11072022_long_balls.png",
    #     dpi=600,
    #     facecolor="#EFE9E6",
    #     bbox_inches="tight",
    #     edgecolor="none",
    #     transparent=False
    # )

    # plt.savefig(
    #     "figures/11072022_long_balls_tr.png",
    #     dpi=600,
    #     facecolor="none",
    #     bbox_inches="tight",
    #     edgecolor="none",
    #     transparent=True
    # )

# Base URL to the GitHub repository containing the font files
github_base_url = "https://raw.githubusercontent.com/Razccoo/scout-system/Testing/assets/fonts"

# Temporary directory to store downloaded fonts
temp_dir = "/tmp/fonts"
os.makedirs(temp_dir, exist_ok=True)

# List of font directories and files in the GitHub repository
font_files = [
    "Karla.ttf",
    "DMSans.ttf"
]

# Function to download a file from GitHub
def download_file(url, save_path):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    with open(save_path, 'wb') as file:
        file.write(response.content)

# Download and load fonts
for font_file in font_files:
    font_url = f"{github_base_url}/{font_file}"
    local_font_path = os.path.join(temp_dir, os.path.basename(font_file))
    download_file(font_url, local_font_path)
    fm.fontManager.addfont(local_font_path)
    try:
        fm.FontProperties(weight=os.path.basename(font_file).split("-")[-1].split(".")[0].lower(), fname=os.path.basename(font_file).split("-")[0])
    except Exception:
        continue

plt.style.use("https://raw.githubusercontent.com/Razccoo/scout-system/Testing/assets/stylesheets/soc_base.mplstyle")
plt.rcParams['font.family'] = 'Karla'

st.title("Oyuncu Dağılım Grafiği Programı")
st.subheader("Hazırlayan Alfie (Twitter: @AlfieScouting)")
st.sidebar.header("Seçenekler")

league_list = list(utils.load_lg_data())
params = scatterplot.param_list
params.sort()

selected_league = st.sidebar.selectbox("Lig Seçiniz", league_list, index=(league_list.index("Süper Lig") if "Süper Lig" in league_list else 0))
selected_season = st.sidebar.selectbox("Sezon Seçiniz", utils.load_lg_data(selected_league))
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", schemas.position_options)
x_axis = st.sidebar.selectbox("Yatay (X) Ekseni", params)
y_axis = st.sidebar.selectbox("Dikey (Y) Ekseni", params)
xx, yy = x_axis, y_axis

# Button to reverse X and Y axis variables
if st.sidebar.button("Eksenleri Ters Çevir"):
    st.session_state.swap_axes = not st.session_state.swap_axes
# Swap variables based on session state
if st.session_state.swap_axes:
    xx, yy = yy, xx

if st.sidebar.button("Radar Oluştur"):
    df = utils.load_player_data(selected_league, selected_season)
    st.pyplot(plot_scatter(df, xx, yy, selected_league, selected_position, selected_season), dpi=400)
