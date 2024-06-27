import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
import numpy as np
import seaborn as sns

# Configuring Seaborn style
sns.set_style("white")

# Caching the data read function
@st.cache_data(ttl=6*60*60)
def read_csv(link):
    return pd.read_csv(link, encoding='utf-8-sig')

# Custom function to filter the dataframe by position
def filter_by_position(df, position):
    position_dict = {
        "Midfielders": ["DMF", "CMF", "AMF"]
    }
    if position in position_dict:
        return df[df['Main Position'].str.contains('|'.join(position_dict[position]), na=False)]
    return df

# Function to create radar chart
def create_pizza_chart(playerdata, player_name, season, img_url):
    # Load fonts
    font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf')
    font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Italic.ttf')
    font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf')

    # Load player image
    player_image = Image.open(urlopen(img_url))

    # Extract the player's data
    player_stats = playerdata[playerdata['Full name'] == player_name].iloc[0]
    team_name = player_stats['Team']

    # Combine all parameters and determine slice and text colors
    params = [
        "Smart passes per 90", "Key passes per 90", "xA per 90", "Shot assists per 90", "Second assists per 90", "Deep completions per 90",
        "Vertical passes per 90", "Short / medium passes per 90", "Accurate short / medium passes, %", "Long passes per 90", "Accurate long passes, %", "Crosses per 90", "Accurate crosses, %",
        "Goals per Shot on Target %", "npxG per shot", "Non-penalty goals per 90", "Shots on target, %", "Assists per 90",
        "pAdj Tkl+Int per 90", "Fouls per 90", "Duels per 90", "Aerial duels won, %", "Duels won, %",
        "Accelerations per 90", "Progressive runs per 90", "Progressive passes per 90", "Dribbles per 90", "Successful dribbles, %"
    ]

    values = [player_stats[param] for param in params]

    slice_colors = ["#1A78CF"] * 6 + ["#FF9300"] * 7 + ["#D70232"] * 5 + ["#32CD32"] * 5
    text_colors = ["#000000"] * 13 + ["#F2F2F2"] * 5 + ["#000000"] * 5

    # Instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#EBEBE9",     # background color
        straight_line_color="#EBEBE9",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    # Plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space="same",        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values
    )

    # Add title
    fig.text(
        0.515, 0.975, f"{player_name} - {team_name}", size=16,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )

    # Add subtitle
    fig.text(
        0.515, 0.953,
        f"Percentile Rank vs Top-Five League Midfielders | Season {season}",
        size=13,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )

    # Add credits
    CREDIT_1 = "data: statsbomb viz fbref"
    CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"

    fig.text(
        0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=9,
        fontproperties=font_italic.prop, color="#000000",
        ha="right"
    )

    # Add text for categories
    fig.text(
        0.34, 0.925, "Vision        Passing       Quality Final Action      Aggression       Build-Up", size=14,
        fontproperties=font_bold.prop, color="#000000"
    )

    # Add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.30, 0.9225), 0.055, 0.021, fill=True, color="#1a78cf",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.41, 0.9225), 0.057, 0.021, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.523, 0.9225), 0.095, 0.021, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.643, 0.9225), 0.080, 0.021, fill=True, color="#32CD32",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.763, 0.9225), 0.047, 0.021, fill=True, color="#8A2BE2",
            transform=fig.transFigure, figure=fig
        ),
    ])

    # Add player image
    ax_image = add_image(
        player_image, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
    )

    plt.show()
    
# Streamlit app layout
st.title('Soccer Prospect Research & Radar Chart Creation')
st.subheader("All data from Wyscout")
st.subheader('Created by Ben Griffis (Twitter: @BeGriffis)')

# Sidebar for user inputs
with st.sidebar:
    st.header('Choose Gender')
    gender = st.selectbox('Gender', ('Men', 'Women'))

# Load league lookup based on gender
if gender == 'Men':
    lg_lookup = read_csv('https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv')
elif gender == 'Women':
    lg_lookup = read_csv('https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup_women.csv')

leagues = lg_lookup.League.unique().tolist()

with st.sidebar:
    league = st.selectbox('League', (leagues))

with st.sidebar:
    with st.form('Choose Basic Options'):
        st.header('Choose Basic Options')
        season = st.selectbox('Season', (lg_lookup[lg_lookup['League'] == league].Season.unique().tolist()))
        position = "Midfielders"  # Hardcoded to Midfielders as per requirement

        min_played = st.slider('Minimum Minutes Played', min_value=0, max_value=1500, step=10)
        max_age = st.slider('Maximum Player Age', min_value=0, max_value=45, step=1)
        min_age = st.slider('Minimum Player Age', min_value=0, max_value=45, step=1)
        show_xtra = st.radio('Show Extra Metrics?', ('No', 'Yes'))

        st.form_submit_button('Submit')

# Load player data
full_league_name = lg_lookup[(lg_lookup['League'] == league) & (lg_lookup['Season'] == season)].League_name.values[0]
file_url = lg_lookup[(lg_lookup['League'] == league) & (lg_lookup['Season'] == season)].FileURL.values[0]

players = read_csv(file_url)

# Apply filters
players = players[(players['Age'] <= max_age) & (players['Age'] >= min_age)]
players = players[(players['Minutes played'] >= min_played)]
players = filter_by_position(players, position)
players['Selected'] = False
players = players.reset_index(drop=True)

# Sidebar for color options and sorting
with st.sidebar:
    st.header('Choose Color Options')
    colors = st.selectbox('Bar Colors', ('Benchmarking Percentiles', 'Metric Groups'))
    callout = st.selectbox('Values Shown', ('Percentile', 'Per 90'))
    metric = st.selectbox('Sort By', sorted(players.columns[3:]))

# Sliders for filtering players based on metrics
with st.sidebar:
    with st.form('Choose Metrics'):
        st.header('Choose Metrics')
        st.button("Reset Sliders", on_click=_update_slider, args=(0,))

        sliders = [
            st.slider('Smart Pass', min_value=0, max_value=100, value=st.session_state.get("slider1", 0)),
            st.slider('Key Pass', min_value=0, max_value=100, value=st.session_state.get("slider2", 0)),
            st.slider('xA', min_value=0, max_value=100, value=st.session_state.get("slider3", 0)),
            st.slider('Shot Assist', min_value=0, max_value=100, value=st.session_state.get("slider4", 0)),
            st.slider('Second Assists', min_value=0, max_value=100, value=st.session_state.get("slider5", 0)),
            st.slider('Deep Completion', min_value=0, max_value=100, value=st.session_state.get("slider6", 0)),
            st.slider('Vertical Pass %', min_value=0, max_value=100, value=st.session_state.get("slider7", 0)),
            st.slider('Short & Medium Pass', min_value=0, max_value=100, value=st.session_state.get("slider8", 0)),
            st.slider('Short & Medium Pass Accuracy', min_value=0, max_value=100, value=st.session_state.get("slider9", 0)),
            st.slider('Long Pass', min_value=0, max_value=100, value=st.session_state.get("slider10", 0)),
            st.slider('Long Pass Accuracy', min_value=0, max_value=100, value=st.session_state.get("slider11", 0)),
            st.slider('Cross', min_value=0, max_value=100, value=st.session_state.get("slider12", 0)),
            st.slider('Cross Accuracy', min_value=0, max_value=100, value=st.session_state.get("slider13", 0)),
            st.slider('Goals/Shot on Target %', min_value=0, max_value=100, value=st.session_state.get("slider14", 0)),
            st.slider('npxG per shot', min_value=0, max_value=100, value=st.session_state.get("slider15", 0)),
            st.slider('Non-Pen Goals', min_value=0, max_value=100, value=st.session_state.get("slider16", 0)),
            st.slider('Shots on Target', min_value=0, max_value=100, value=st.session_state.get("slider17", 0)),
            st.slider('Assist', min_value=0, max_value=100, value=st.session_state.get("slider18", 0)),
            st.slider('PAdj Tkl+Int', min_value=0, max_value=100, value=st.session_state.get("slider19", 0)),
            st.slider('Fouls', min_value=0, max_value=100, value=st.session_state.get("slider20", 0)),
            st.slider('Duels', min_value=0, max_value=100, value=st.session_state.get("slider21", 0)),
            st.slider('Aerial Duels Win %', min_value=0, max_value=100, value=st.session_state.get("slider22", 0)),
            st.slider('Duels Win %', min_value=0, max_value=100, value=st.session_state.get("slider23", 0)),
            st.slider('Accelerations', min_value=0, max_value=100, value=st.session_state.get("slider24", 0)),
            st.slider('Progressive Runs', min_value=0, max_value=100, value=st.session_state.get("slider25", 0)),
            st.slider('Progressive Pass', min_value=0, max_value=100, value=st.session_state.get("slider26", 0)),
            st.slider('Dribbles', min_value=0, max_value=100, value=st.session_state.get("slider27", 0)),
            st.slider('Dribble Win %', min_value=0, max_value=100, value=st.session_state.get("slider28", 0)),
        ]

        st.form_submit_button('Submit')

# Filter dataframe based on slider values
for slider, label in zip(sliders, params):
    players = players[players[label] >= slider]

# Select player for radar chart
with st.sidebar:
    player_name = st.selectbox('Player Name', players['Full name'].unique().tolist())
    player_team = players[players['Full name'] == player_name]['Team'].unique().tolist()[0]
    player_age = players[players['Full name'] == player_name]['Age'].unique().tolist()[0]

# Generate radar chart
if st.sidebar.button('Generate Radar'):
    create_pizza_chart(
        playerdata=players,
        player_name=player_name,
        season=season,
        img_url="https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
    )
