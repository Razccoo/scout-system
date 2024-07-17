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
import matplotlib.gridspec as gridspec
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from io import BytesIO

from mplsoccer import Pitch

from PIL import Image
import urllib
import os

st.set_page_config(page_title="Dagilim Grafikleri")

if 'swap_axes' not in st.session_state:
    st.session_state.swap_axes = False
    
def plot_scatter(df, xx, yy, selected_league, selected_position, selected_season, use_images=True, dpi=400):
    plt.clf()
    plt.style.use('fivethirtyeight')

    # Function to download image from URL
    def download_image(url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    # Function to resize images to fit within the figure
    def resize_image_to_fit(image, fig_width, fig_height, dpi):
        total_width = image.size[0]
        max_height = image.size[1]

        # Calculate the scaling factor to fit the images within the figure
        scale = min(fig_width * dpi / total_width, fig_height * dpi / max_height)

        # Resize images
        resized_image = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)), Image.LANCZOS)

        return resized_image

    fig_width, fig_height = 14, 8

    df = utils.filter_by_position(df, selected_position)
    df.rename(columns=schemas.column_mapping(), inplace=True)
    df_plot = df[(df['Oynadığı dakikalar'] >= df['Oynadığı dakikalar'].median()) & (df[xx] >= df[xx].median())]

    df_plot['zscore'] = stats.zscore(df_plot[xx]) * 0.6 + stats.zscore(df_plot[yy]) * 0.4
    df_plot['annotated'] = [True if x > df_plot['zscore'].quantile(0.8) else False for x in df_plot['zscore']]
    
    if use_images:
        # Load images using PIL
        url1 = 'https://raw.githubusercontent.com/Razccoo/scout-system/Testing/IMG_5349.png'
        url2 = 'https://raw.githubusercontent.com/Razccoo/scout-system/Testing/IMG_5348.png'

        # Download the images
        image1 = download_image(url1)
        image2 = download_image(url2)

        # Resize images to fit the figure size
        resized_image1 = resize_image_to_fit(image1, fig_width, fig_height, dpi)
        resized_image2 = resize_image_to_fit(image2, fig_width, fig_height, dpi)

        # Convert images to numpy arrays
        image1_array = np.array(resized_image1)
        image2_array = np.array(resized_image2)

        # Create a figure
        fig = plt.figure(figsize=(fig_width, fig_height))

        ax = fig.add_axes([0, 0, 1, 1], zorder=1, frameon=False)
        ax.axis('off')
        ax2 = fig.add_axes([0.28, 0, 0.45, 0.9], zorder=0)

        # Add the first image on the figure
        fig.figimage(image1_array, xo=-600, yo=-100, alpha=1, zorder=1)

        # Add the second image on the figure
        fig.figimage(image2_array, xo=image1_array.shape[1] + 2300, yo=-100, alpha=1, zorder=1)
    else:
        fig = plt.figure(figsize=(8, 8))
        ax2 = fig.add_axes([0, 0, 1, 0.9], zorder=0)

    ax2.grid(visible=True, ls='--', color='lightgrey')

    ax2.scatter(
        df_plot[xx], df_plot[yy],
        c=df_plot['zscore'], cmap='inferno',
        zorder=3, ec='grey', s=55, alpha=0.8
    )

    # Function to clean up variable names
    def clean_variable_name(name):
        return name.replace(" / 90", "")

    xx_cleaned = clean_variable_name(xx)
    yy_cleaned = clean_variable_name(yy)

    texts = []
    annotated_df = df_plot[df_plot['annotated']].reset_index(drop=True)
    for index in range(annotated_df.shape[0]):
        texts += [
            ax2.text(
                x=annotated_df[xx].iloc[index], y=annotated_df[yy].iloc[index],
                s=f"{annotated_df['Oyuncu'].iloc[index]}",
                path_effects=[path_effects.Stroke(linewidth=2, foreground=fig.get_facecolor()), path_effects.Normal()],
                color='black',
                family='DMSans', weight='bold'
            )
        ]

    adjust_text(texts, only_move={'points': 'y', 'text': 'xy', 'objects': 'xy'})

    ax2.set_ylabel(ylabel=f'{yy}', weight='bold')
    ax2.set_xlabel(xlabel=f'{xx}', weight='bold')
    
    if use_images:
        fig_text(
            x=0.25, y=0.99,
            s=f"{selected_league} {selected_position}",
            va="bottom", ha="left",
            fontsize=20, color="black", font="DMSans", weight="bold"
        )

        fig_text(
            x=0.25, y=0.91,
            s=f"{xx_cleaned} ve {yy_cleaned}\nYalnızca ortanca üzerinde süre alan ve {xx_cleaned.lower()} yapan oyuncular gösterilmiştir.\nHazırlayan @alfiescouting | {selected_season} sezonu",
            va="bottom", ha="left",
            fontsize=12, color="#5A5A5A", font="Karla"
        )
    else:
        fig_text(
            x=0.0, y=0.99,
            s=f"{selected_league} {selected_position}",
            va="bottom", ha="left",
            fontsize=20, color="black", font="DMSans", weight="bold"
        )

        fig_text(
            x=0.0, y=0.91,
            s=f"{xx_cleaned} ve {yy_cleaned}\nYalnızca ortanca üzerinde süre alan ve {xx_cleaned.lower()} yapan oyuncular gösterilmiştir.\nHazırlayan @alfiescouting | {selected_season} sezonu",
            va="bottom", ha="left",
            fontsize=12, color="#5A5A5A", font="Karla"
        )
        
    return fig

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
    st.pyplot(plot_scatter(df, xx, yy, selected_league, selected_position, selected_season, use_images=False), dpi=400)