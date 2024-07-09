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


from mplsoccer import Pitch

from PIL import Image
import urllib
import os

# URL to the GitHub repository containing the font files
github_repo_url = "https://github.com/Razccoo/scout-system/tree/Testing/assets"

# Function to download a file from GitHub
def download_file(url, save_path):
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    with open(save_path, 'wb') as file:
        file.write(response.content)

# Temporary directory to store downloaded fonts
temp_dir = "/tmp/fonts"
os.makedirs(temp_dir, exist_ok=True)

# List of font directories in the GitHub repository
font_dirs = ["Karla.ttf", "DMSans.ttf"]  # Update with your actual directories

for font_dir in font_dirs:
    font_url = f"{github_repo_url}/{font_dir}?raw=true"
    response = requests.get(font_url)
    response.raise_for_status()
    for line in response.text.splitlines():
        if 'href' in line and '.ttf' in line:
            font_file = line.split('href="')[1].split('"')[0]
            font_name = font_file.split('/')[-1]
            local_font_path = os.path.join(temp_dir, font_name)
            download_file(f"{github_repo_url}/{font_dir}/{font_file}", local_font_path)
            fm.fontManager.addfont(local_font_path)
            try:
                fm.FontProperties(weight=font_name.split("-")[-1].split(".")[0].lower(), fname=font_name.split("-")[0])
            except Exception:
                continue