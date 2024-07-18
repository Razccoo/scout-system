import os
import requests
from io import BytesIO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.font_manager as fm
from PIL import Image
from highlight_text import fig_text
from adjustText import adjust_text
from mplsoccer import Pitch
import scipy.stats as stats
import streamlit as st

from scripts import utils, schemas, scatterplot

# Configure the Streamlit page
st.set_page_config(page_title="Dagilim Grafikleri")

# Initialize session state for swapping axes
if 'swap_axes' not in st.session_state:
    st.session_state.swap_axes = False

# Define utility functions
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def resize_image_to_fit(image, fig_width, fig_height, dpi):
    total_width = image.size[0]
    max_height = image.size[1]
    scale = min(fig_width * dpi / total_width, fig_height * dpi / max_height)
    resized_image = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)), Image.LANCZOS)
    return resized_image

def clean_variable_name(name):
    return name.replace(" / 90", "")

def download_fonts(font_files, github_base_url, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    for font_file in font_files:
        font_url = f"{github_base_url}/{font_file}"
        local_font_path = os.path.join(temp_dir, os.path.basename(font_file))
        download_file(font_url, local_font_path)
        fm.fontManager.addfont(local_font_path)

def download_file(url, save_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as file:
        file.write(response.content)

# Plot scatter function
def plot_scatter(df, xx, yy, selected_league, selected_position, selected_season, use_images=False, dpi=400):
    plt.clf()
    plt.style.use('fivethirtyeight')
    
    fig_width, fig_height = 14, 8
    df = utils.filter_by_position(df, selected_position)
    df.rename(columns=schemas.column_mapping(), inplace=True)
    df_plot = df[(df['Oynadığı dakikalar'] >= df['Oynadığı dakikalar'].median()) & (df[xx] >= df[xx].median())]
    
    df_plot['zscore'] = stats.zscore(df_plot[xx]) * 0.6 + stats.zscore(df_plot[yy]) * 0.4
    df_plot['annotated'] = [x > df_plot['zscore'].quantile(0.8) for x in df_plot['zscore']]
    
    fig = plt.figure(figsize=(fig_width, fig_height))

    if use_images:
        url1 = 'https://raw.githubusercontent.com/Razccoo/scout-system/Testing/IMG_5349.png'
        url2 = 'https://raw.githubusercontent.com/Razccoo/scout-system/Testing/IMG_5348.png'
        image1 = download_image(url1)
        image2 = download_image(url2)
        resized_image1 = resize_image_to_fit(image1, fig_width, fig_height, dpi)
        resized_image2 = resize_image_to_fit(image2, fig_width, fig_height, dpi)
        image1_array = np.array(resized_image1)
        image2_array = np.array(resized_image2)
        ax = fig.add_axes([0, 0, 1, 1], zorder=1, frameon=False)
        ax.axis('off')
        fig.figimage(image1_array, xo=-600, yo=-100, alpha=1, zorder=1)
        fig.figimage(image2_array, xo=image1_array.shape[1] + 2300, yo=-100, alpha=1, zorder=1)
        ax2 = fig.add_axes([0.28, 0, 0.45, 0.9], zorder=0)
    else:
        ax2 = fig.add_axes([0.0, 0, 1, 0.9], zorder=0)
        
    ax2.grid(visible=True, ls='--', color='lightgrey')
    ax2.scatter(
        df_plot[xx], df_plot[yy],
        c=df_plot['zscore'], cmap='inferno',
        zorder=3, ec='grey', s=55, alpha=0.8
    )
    
    xx_cleaned = clean_variable_name(xx)
    yy_cleaned = clean_variable_name(yy)
    
    texts = []
    annotated_df = df_plot[df_plot['annotated']].reset_index(drop=True)
    for index in range(annotated_df.shape[0]):
        texts.append(
            ax2.text(
                x=annotated_df[xx].iloc[index], y=annotated_df[yy].iloc[index],
                s=f"{annotated_df['Oyuncu'].iloc[index]}",
                path_effects=[path_effects.Stroke(linewidth=2, foreground=fig.get_facecolor()), path_effects.Normal()],
                color='black', family='DMSans', weight='bold'
            )
        )
    
    adjust_text(texts, only_move={'points': 'y', 'text': 'xy', 'objects': 'xy'})
    ax2.set_ylabel(ylabel=f'{yy}', weight='bold')
    ax2.set_xlabel(xlabel=f'{xx}', weight='bold')
    
    if use_images:
        text_x = 0.25
    else:
        text_x = 0.0
        
    fig_text(
        x=text_x, y=0.99,
        s=f"{selected_league} {selected_position}",
        va="bottom", ha="left",
        fontsize=20, color="black", font="DMSans", weight="bold"
    )
    
    fig_text(
        x=text_x, y=0.91,
        s=f"{xx_cleaned} ve {yy_cleaned}\nYalnızca ortanca üzerinde süre alan ve {xx_cleaned.lower()} yapan oyuncular gösterilmiştir.\nHazırlayan @alfiescouting | {selected_season} sezonu",
        va="bottom", ha="left",
        fontsize=12, color="#5A5A5A", font="Karla"
    )
    
    return fig

# Download fonts
github_base_url = "https://raw.githubusercontent.com/Razccoo/scout-system/Testing/assets/fonts"
temp_dir = "/tmp/fonts"
font_files = ["Karla.ttf", "DMSans.ttf"]
download_fonts(font_files, github_base_url, temp_dir)

plt.style.use("https://raw.githubusercontent.com/Razccoo/scout-system/Testing/assets/stylesheets/soc_base.mplstyle")
plt.rcParams['font.family'] = 'Karla'

# Streamlit UI
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

# Generate scatter plot
if st.sidebar.button("Radar Oluştur"):
    df = utils.load_player_data(selected_league, selected_season)
    st.pyplot(plot_scatter(df, xx, yy, selected_league, selected_position, selected_season, use_images=False), dpi=400)
