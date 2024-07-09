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


from mplsoccer import Pitch

from PIL import Image
import urllib
import os

fm.FontManager.addfont(f"")
font_path = "../assets"
# for x in os.listdir(font_path):
#     for y in os.listdir(f"{font_path}/{x}"):
#         if y.split(".")[-1] == "ttf":
#             fm.fontManager.addfont(f"{font_path}/{x}/{y}")
#             try:
#                 fm.FontProperties(weight=y.split("-")[-1].split(".")[0].lower(), fname=y.split("-")[0])
#             except Exception:
#                 continue

plt.style.use("../assets/stylesheets/soc_base.mplstyle")
plt.rcParams['font.family'] = 'Karla'