# utils.py
import pandas as pd
import numpy as np
from scripts import schemas
from scipy import stats
from mplsoccer import Radar, FontManager, grid
from PIL import Image
import textwrap
import matplotlib.pyplot as plt
from highlight_text import fig_text
import streamlit as st
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from urllib.request import urlopen

font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                        'src/hinted/Roboto-Regular.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                        'src/hinted/Roboto-Italic.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab[wght].ttf')

league_info_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv'
def scout_report(df):
    df["name"] = df["name"].replace(schemas.column_mapping())
    df["name"] = df["name"].replace(schemas.label_mapping())
    RAW_VALUES = df["raw_value"].values
    VALUES = df["value"].values
    LABELS = df["name"].values
    GROUP = df["group"].values
    OFFSET = np.pi / 2

    PAD = 2
    ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
    ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
    WIDTH = (2 * np.pi) / len(ANGLES)

    GROUPS_SIZE = [len(i[1]) for i in df.groupby("group")]

    offset = 0
    IDXS = []
    for size in GROUPS_SIZE:
        IDXS += list(range(offset + PAD, offset + size + PAD))
        offset += size + PAD

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": "polar"})
    fig.subplots_adjust(top=0.85)
    ax.set_theta_offset(OFFSET)
    ax.set_ylim(-.5, 1)
    ax.set_frame_on(False)
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

    ax.bar(
        ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS, 
        edgecolor="#4A2E19", linewidth=1
    )

    offset = 0 
    for group, size in zip(GROUPS_SIZE, GROUPS_SIZE):
        x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
        ax.plot(x1, [-.02] * 50, color="#4A2E19")
        
        x2 = np.linspace(ANGLES[offset], ANGLES[offset + PAD - 1], num=50)
        ax.plot(x2, [.2] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.4] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.60] * 50, color="#bebebe", lw=0.8)
        ax.plot(x2, [.80] * 50, color="#bebebe", lw=0.8)
        x3 = np.linspace(0, 2 * np.pi, num=50)  # Full circle
        ax.plot(x3, [1] * 50, color="#bebebe", lw=0.8)

        offset += size + PAD
    
    text_cs = []
    text_inv_cs = []
    for i, bar in enumerate(ax.patches):
        pc = 1 - bar.get_height()

        if pc <= 0.1:
            color = ('#01349b', '#d9e3f6')  # Elite
        elif 0.1 < pc <= 0.35:
            color = ('#007f35', '#d9f0e3')  # Above Avg
        elif 0.35 < pc <= 0.66:
            color = ('#9b6700', '#fff2d9')  # Avg
        else:
            color = ('#b60918', '#fddbde')  # Below Avg

        bar.set_color(color[1])
        bar.set_edgecolor(color[0])

        text_cs.append(color[0])
        text_inv_cs.append(color[1])
        
    for i, bar in enumerate(ax.patches):
        value_format = f"{RAW_VALUES[i]:.2f}"
        color = text_inv_cs[i]
        face = text_cs[i]

        ax.annotate(value_format,
                    (bar.get_x() + bar.get_width() / 2, bar.get_height() - 0.1),
                    ha='center', va='center', size=10, xytext=(0, 8),
                    textcoords='offset points', color=color,
                    bbox=dict(boxstyle="round", fc=face, ec="black", lw=1))
        
    # Function to wrap labels
    def wrap_labels(labels, width):
        wrapped = []
        for label in labels:
            if label not in schemas.label_mapping().values():
                wrapped.append('\n'.join(textwrap.wrap(label, width)))
            else:
                wrapped.append(label)
        return wrapped
    
    wrapped_labels = wrap_labels(LABELS, 10)
    
    add_labels(ANGLES[IDXS], VALUES, wrapped_labels, OFFSET, ax, text_cs)
    
    PAD = 0.02
    ax.text(0.15, 0 + PAD, "0", size=10, color='#4A2E19')
    ax.text(0.15, 0.2 + PAD, "20", size=10, color='#4A2E19')
    ax.text(0.15, 0.4 + PAD, "40", size=10, color='#4A2E19')
    ax.text(0.15, 0.6 + PAD, "60", size=10, color='#4A2E19')
    ax.text(0.15, 0.8 + PAD, "80", size=10, color='#4A2E19')
    ax.text(0.15, 1 + PAD, "100", size=10, color='#4A2E19')
    
    ax.set_facecolor('#fbf9f4')
    fig = plt.gcf()
    fig.patch.set_facecolor('#fbf9f4')
    fig.set_size_inches(12, (12*.9)) #length, height

    fig_text(
        0.88, 0.055, "Data WyScout\nHazırlayan @AlfieScouting\nTasarım @BeGriffis\n\n<Elit (En Üst 10%)>\n<Ortalama Üstü (11-35%)>\n<Ortalama (36-66%)>\n<Ortalama Altı (En Alt 35%)>", color="#4A2E19",
        highlight_textprops=[{"color": '#01349b'},
                             {'color' : '#007f35'},
                             {"color" : '#9b6700'},
                             {'color' : '#b60918'},
                            ],
        size=10, fig=fig, ha='right',va='center'
    )
    
    return fig, ax

def get_label_rotation(angle, offset):
    rotation = np.rad2deg(angle + offset) + 90
    if angle <= np.pi / 2:
        alignment = "center"
        rotation = rotation + 180
    elif 4.5 < angle < np.pi * 2:
        alignment = "center"
        rotation = rotation - 180
    else: 
        alignment = "center"
    return rotation, alignment

def add_labels(angles, values, labels, offset, ax, text_colors):
    padding = .05
    
    for angle, value, label, text_col in zip(angles, values, labels, text_colors):
        angle = angle
        
        rotation, alignment = get_label_rotation(angle, offset)

        ax.text(
            x=angle, 
            y=1.10,
            s=label, 
            ha=alignment, 
            va="center", 
            rotation=rotation,
            color=text_col,
        )

def filter_by_position(df, position):
    fw = ["CF", "RW", "LW", "AMF"]
    if position == "Forvetler (OOS, K, SF)":
        return df[df['Main Position'].str.contains('|'.join(fw), na=False)]
    
    stw = ["CF", "RW", "LW", "LAMF", "RAMF"]
    if position == "Forvetler ve Kanatlar":
        return df[df['Main Position'].str.contains('|'.join(stw), na=False)]
    
    fwns = ["RW", "LW", "AMF"]
    if position == "Santrforsuz Forvetler (OOS, K)":
        return df[df['Main Position'].str.contains('|'.join(fwns), na=False)]
    
    wing = ["RW", "LW", "WF", "LAMF", "RAMF"]
    if position == "Kanatlar":
        return df[df['Main Position'].str.contains('|'.join(wing), na=False)]

    mids = ["DMF", "CMF", "AMF"]
    if position == "Orta Saha (DOS, OS, OOS)":
        return df[df['Main Position'].str.contains('|'.join(mids), na=False)]

    cms = ["CMF", "AMF"]
    if position == "DOS Olmayan Orta Saha (OS, OOS)":
        return df[df['Main Position'].str.contains('|'.join(cms), na=False)]

    dms = ["CMF", "DMF"]
    if position == "OOS Olmayan Orta Saha (DOS, OS)":
        return df[df['Main Position'].str.contains('|'.join(dms), na=False)]

    fbs = ["LB", "RB", "WB"]
    if position == "Bekler (FB/KB)":
        return df[df['Main Position'].str.contains('|'.join(fbs), na=False)]

    defs = ["LB", "RB", "WB", "CB", "DMF"]
    if position == "Defansif Oyuncular (STP, FB/KB, DOS)":
        return df[df['Main Position'].str.contains('|'.join(defs), na=False)]

    cbdm = ["CB", "DMF"]
    if position == "Stoper & Defansif Orta Saha":
        return df[df['Main Position'].str.contains('|'.join(cbdm), na=False)]

    cf = ["CF"]
    if position == "Santrforlar":
        return df[df['Main Position'].str.contains('|'.join(cf), na=False)]

    cb = ["CB"]
    if position == "Stoperler":
        return df[df['Main Position'].str.contains('|'.join(cb), na=False)]
    else:
        return df

@st.cache_data(ttl=6*60*60)
def load_top_5_leagues(season_selection=None):
    top_5_leagues = ["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1"]
    if season_selection is None:
        season_selection = ["22-23", "23-24"]  # Default seasons if none are provided
    

    top_5_league_data = pd.DataFrame()
    for league in top_5_leagues:
        for season in season_selection:
            league_file = f"{league} {season}.csv".replace(" ", "%20").replace("ü", "u").replace("ó", "o").replace("ö", "o").replace("ã", "a")
            league_data = read_csv2(f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{league_file}')
            league_data['League'] = league
            league_data['Season'] = season
            league_data = league_data[list(schemas.column_mapping().keys())]
            top_5_league_data = pd.concat([top_5_league_data, league_data], ignore_index=True)
    return top_5_league_data

@st.cache_data(ttl=6*60*60)
# Function to load data for the Top 9 Leagues
def load_top_9_leagues(season_selection=None):
    top_9_leagues = ["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1", "Süper Lig", "Eredivisie", "Primeira Liga", "Belgian Pro League", "Saudi Pro League"]
    if season_selection is None:
        season_selection = ["22-23", "23-24"]
        
    top_9_league_data = pd.DataFrame()
    for league in top_9_leagues:
        for season in season_selection:
            league_file = f"{league} {season}.csv".replace(" ", "%20").replace("ü", "u").replace("ó", "o").replace("ö", "o").replace("ã", "a")
            league_data = read_csv2(f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{league_file}')
            league_data['League'] = league
            league_data['Season'] = season
            league_data = league_data[list(schemas.column_mapping().keys())]
            top_9_league_data = pd.concat([top_9_league_data, league_data], ignore_index=True)
    return top_9_league_data


def read_csv(link):
    return pd.read_csv(link,encoding='utf-8-sig')

def read_csv2(link):
    df = pd.read_csv(link,encoding='utf-8-sig')
    df['pAdj Tkl+Int per 90'] = df['PAdj Sliding tackles'] + df['PAdj Interceptions']
    df['1st, 2nd, 3rd assists'] = df['Assists per 90'] + df['Second assists per 90'] + df['Third assists per 90']
    df['xA per Shot Assist'] = df['xA per 90'] / df['Shot assists per 90']
    df['xA per Shot Assist'] = [0 if df['Shot assists per 90'][i]==0 else df['xA per 90'][i] / df['Shot assists per 90'][i] for i in range(len(df))]
    df['Aerial duels won per 90'] = df['Aerial duels per 90'] * (df['Aerial duels won, %']/100)
    df['Cards per 90'] = df['Yellow cards per 90'] + df['Red cards per 90']
    df['Clean sheets, %'] = df['Clean sheets'] / df['Matches played']
    df['npxG'] = df['xG'] - (.76 * df['Penalties taken'])
    df['npxG per 90'] = df['npxG'] / (df['Minutes played'] / 90)
    df['npxG per shot'] = df['npxG'] / (df['Shots'] - df['Penalties taken'])
    df['npxG per shot'] = [0 if df['Shots'][i]==0 else df['npxG'][i] / (df['Shots'][i] - df['Penalties taken'][i]) for i in range(len(df))]
    df['Vertical Pass %'] = df['Vertical passes per 90'] / df['Passes per 90']
    
    df = df.dropna(subset=['Position', 'Team within selected timeframe', 'Age']).reset_index(drop=True)
    df = df.dropna(subset=['Position']).reset_index(drop=True)
    df['Main Position'] = df['Position'].str.split().str[0].str.rstrip(',')
    df = df.dropna(subset=['Main Position']).reset_index(drop=True)
    position_replacements = {
        'LAMF': 'LW',
        'RAMF': 'RW',
        'LCB3': 'LCB',
        'RCB3': 'RCB',
        'LCB5': 'LCB',
        'RCB5': 'RCB',
        'LB5': 'LB',
        'RB5': 'RB',
        'RWB': 'RB',
        'LWB': 'LB'
    }
    
    df['Main Position'] = df['Main Position'].replace(position_replacements)
    df.fillna(0,inplace=True)
    # df.rename(columns=schemas.column_mapping(), inplace=True)
  
    return df

def rank_column(df, column_name):
    return stats.rankdata(df[column_name], "average") / len(df[column_name])

def calculate_score(df, schema):
    for category, details in schema.items():
        weight = details['weight']
        for metric in details['measurements'].keys():
            if metric in df.columns:
                df[metric + '_z'] = stats.zscore(df[metric].astype(float))
                df[metric + '_z'] = scale_z_to_100(df[metric + '_z'].astype(float))
        for metric, metric_weight in details['measurements'].items():
            if metric + '_z' in df.columns:
                df[category + '_score'] = df.get(category + '_score', 0) + df[metric + '_z'] * metric_weight
        df[category + '_score'] *= weight
    df['total_score'] = df[[category + '_score' for category in schema.keys()]].sum(axis=1)
    return df

# Function to scale z-score to 100-point scale
def scale_z_to_100(z):
    min_z = z.min()
    max_z = z.max()
    return ((z - min_z) / (max_z - min_z)) * 100

@st.cache_data(ttl=6*60*60)
def load_lg_data(selected_league = None):
    league_data = read_csv(league_info_url)
    leagues = league_data['League'].unique()
    if selected_league != None:
        filtered_season = league_data[league_data['League'] == selected_league]['Season'].sort_values(ascending=False).unique()
        return filtered_season
    else:      
        return leagues

@st.cache_data(ttl=6*60*60)    
def load_player_data(selected_league, selected_season):
    full_league_name = f"{selected_league} {selected_season}"
    league_season_data = read_csv2((f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{full_league_name.replace(" ","%20").replace("ü","u").replace("ó","o").replace("ö","o").replace("ã","%C3%A3")}.csv'))
    league_season_data['League'] = f'{selected_league}'
    league_season_data['Season'] = f'{selected_season}'
    league_season_data = league_season_data[list(schemas.column_mapping().keys())]
    return league_season_data

def filter_data(league_season_data, selected_position, min_minutes_played, max_age):
    top_5_league_data = filter_by_position(load_top_5_leagues(), selected_position)
    top_5_league_data = top_5_league_data[
        (top_5_league_data['Minutes played'] >= min_minutes_played) &
        (top_5_league_data['Age'] <= max_age)
    ].reset_index(drop=True)

    filtered_data = filter_by_position(league_season_data, selected_position)
    filtered_data = filtered_data[
        (filtered_data['Minutes played'] >= min_minutes_played) &
        (filtered_data['Age'] <= max_age)
    ].reset_index(drop=True)
    return filtered_data, top_5_league_data

def selected_player_data(filtered_data, comparison_data, player_name, player_age, max_age, selected_comparison, selected_schema, selected_league, selected_season, selected_position, player_image = None):
    player_data = filtered_data[
        (filtered_data['Player'] == player_name) &
        (filtered_data['Age'] == player_age)]
    player_main_position = filtered_data.loc[filtered_data['Player'] == player_name, 'Main Position'].values[0]

    # Determine schema based on player's main position
    selected_schema_type = schemas.position_to_schema().get(player_main_position)
    
    # Initialize combined_data
    combined_data = pd.DataFrame()

    # Check if the player is already playing in the top 5 leagues
    player_in_top_5 = any(player_data['League'].isin(["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1"]))

    if selected_comparison == "Top 5 Ligi":
        if player_in_top_5:
            # Player is already in the top 5 leagues, use filtered data
            combined_data = comparison_data
            player_data = combined_data[
                (combined_data['Player'] == player_name) &
                (combined_data['Age'] == player_age)
            ]
        else:
            # Player is not in the top 5 leagues, combine data
            player_data_temp = filtered_data[
                (filtered_data['Player'] == player_name) &
                (filtered_data['Age'] == player_age)
            ]
            combined_data = pd.concat([comparison_data, player_data_temp]).reset_index(drop=True)
            player_data = combined_data[
                (combined_data['Player'] == player_name) &
                (combined_data['Age'] == player_age)
            ]
    else:
        combined_data = comparison_data
        player_data = combined_data[
            (combined_data['Player'] == player_name) &
            (combined_data['Age'] == player_age)
        ]
    
    # combined_data = calculate_score(combined_data, schemas.att_winger_schema())
    player_pos = player_data['Main Position'].iloc[0]
    player_min = player_data['Minutes played'].iloc[0]
    player_team = player_data['Team within selected timeframe'].iloc[0]
    title_note = " 90 Dakika Başına"
    
    if not player_data.empty:
        st.subheader(f"Data for {player_name} (Age {player_age})")
        st.write(player_data)
        
        # Use selected schema
        if selected_schema == "Default Schema":
            schema_to_use = schemas.schema_params()[selected_schema_type]
        else:
            schema_to_use = st.session_state.custom_schemas[selected_schema]
        
        # Generate radar plot
        radar_values = []
        radar_labels = []
        radar_groups = []
        radar_raw_values = []
        
        for group, metrics in schema_to_use.items():
            for metric in metrics:
                if metric in player_data.columns:
                    player_value = player_data.iloc[0][metric]
                    ranked_values = rank_column(combined_data, metric)
                    player_ranked_value = ranked_values[combined_data.index[combined_data['Player'] == player_name].tolist()[0]]
                    radar_values.append(player_ranked_value)
                    radar_labels.append(metric)
                    radar_groups.append(group)
                    radar_raw_values.append(player_value)
        
        radar_data = pd.DataFrame({
            'value': radar_values,
            'name': radar_labels,
            'group': radar_groups,
            'raw_value': radar_raw_values
        }).sort_values('group')
        
        fig, ax = scout_report(radar_data)
        
        # Common title and annotation settings
        suptitle_common = {
            "fontsize": 15,
            "fontfamily": "DejaVu Sans",
            "color": "#4A2E19", 
            "fontweight": "bold",
            "fontname": "DejaVu Sans",
            "x": 0.5,
            "y": 0.99
        }

        # Compare selected position with the values in the pos_mapping
        for position, schema in schemas.pos_mapping().items():
            if selected_position == position:
                compare_pos = schema
                break
        else:
            compare_pos = selected_position  # Handle case where position is not found

        if selected_comparison == "Top 5 Ligi":
            suptitle_text = f'{player_name} ({player_age}, {player_pos}, {player_min} mins.) | {selected_season} | {player_team}\nTop 5 Lig | {max_age} Yaş Altı | {compare_pos} Karşılaştırarak\nYüzdelik Sıralama | Veriler{title_note}'
            annotate_text = f"Çubuklar yüzdelik dilimlerdir\nGösterilen değerler 90 dk başına\nTop 5 Ligler: Premier League, La Liga,\nBundesliga, Serie A, Ligue 1\nÖrneklem büyüklüğü: ({combined_data.shape[0]} oyuncu)"
        else:
            suptitle_text = f'{player_name} ({player_age}, {player_pos}, {player_min} mins.) | {selected_season} | {player_team}\n{selected_league} | {max_age} Yaş Altı | {compare_pos} Karşılaştırarak\nYüzdelik Sıralama | Veriler{title_note}'
            annotate_text = f"Çubuklar yüzdelik dilimlerdir\nGösterilen değerler 90 dk başına\nÖrneklem büyüklüğü: ({combined_data.shape[0]} oyuncu)"

        plt.suptitle(suptitle_text, **suptitle_common)
        fig.text(x = 0.1, y = 0.03, s = annotate_text, ha='left', va='center',
                    fontsize=10, color="#4A2E19")
        
        if player_image is not None:
            image = Image.open(player_image)
            newax = fig.add_axes([.425, .395, 0.18, 0.18], anchor='C', zorder=1)
            newax.imshow(image)
            newax.axis('off')
            
        fig.text(0.5175, 0.02, "@ALFIESCOUTING", ha='center', va='center', size=26, fontproperties=font_bold.prop) 
    return st.pyplot(fig, dpi=400)

@st.cache_data(ttl=6*60*60)
def load_all_csv_files():
    base_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/'
    # Load the league info
    league_info_df = read_csv(league_info_url)
    
    # Construct the file names
    csv_files = [
        f"{row['League']} {row['Season']}.csv".replace(' ', '%20').replace('ü','u').replace('ó','o').replace('ö','o').replace('ã','%C3%A3')
        for _, row in league_info_df.iterrows()
    ]
    
    data_frames = {}
    for file_name in csv_files:
        file_url = base_url + file_name
        try:
            df = read_csv(file_url)
            data_frames[file_name.replace('%20', ' ')] = df
            print(f"Loaded {file_name.replace('%20', ' ')} successfully.")
        except Exception as e:
            print(f"Failed to load {file_name.replace('%20', ' ')}. Error: {e}")
    
    return data_frames

def pointcolor_selector():
    options = schemas.params_list()
    default_index = options.index("Yaş") if "Yaş" in options else 0
    point_color = st.sidebar.selectbox("Nokta Rengi Değişkeni", options, index=default_index)
    return point_color

def player_comparison_radar(df, players, params, low, high, lower_is_better=None):
    URL1 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
            'SourceSerifPro-Regular.ttf')
    serif_regular = FontManager(URL1)
    URL2 = ('https://raw.githubusercontent.com/googlefonts/SourceSerifProGFVersion/main/fonts/'
            'SourceSerifPro-ExtraLight.ttf')
    serif_extra_light = FontManager(URL2)
    URL3 = ('https://raw.githubusercontent.com/google/fonts/main/ofl/rubikmonoone/'
            'RubikMonoOne-Regular.ttf')
    rubik_regular = FontManager(URL3)
    URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
    robotto_thin = FontManager(URL4)
    URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
            'RobotoSlab%5Bwght%5D.ttf')
    robotto_bold = FontManager(URL5)
    
    if lower_is_better is None:
        lower_is_better = []
        
    # Normalize lower_is_better parameters
    for param in lower_is_better:
        if param in params:
            idx = params.index(param)
            df[param] = df[param].apply(lambda x: -x)
            low[idx] = -high[idx]
            high[idx] = -low[idx]

    player_values = []
    player_teams = []
    for player in players:
        player_values.append(df[df['Oyuncu'] == player][params].iloc[0].tolist())
        player_teams.append(df[df['Oyuncu'] == player]['Kulüp'].iloc[0])
    
    radar = Radar(params, low, high, lower_is_better=lower_is_better,
                  round_int=[False]*len(params), num_rings=4,
                  ring_width=1, center_circle_radius=1)
        
    ###################################################
    # creating the figure using the grid function from mplsoccer:
    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                    title_space=0, endnote_space=0, grid_key='radar', axis=False)
    
    # Create the radar chart
    radar.setup_axis(ax=axs['radar'], facecolor='None')  # format axis as a radar
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#28252C', edgecolor='#39353f')

    # Colors for the players
    edgecolor = ['#FFBF36', '#00E025', '#0020F2', '#DB36FC', '#FF0000']
    colors = ['#FFB464', '#20FF20', '#2C6BFF', '#C962FD', '#FF3859']

    # Plot radar for each player
    for i, player_value in enumerate(player_values):
        radar_output = radar.draw_radar_solid(player_value, ax=axs['radar'],
                                              kwargs={'facecolor': colors[i % len(colors)],
                                                      'alpha': 0.3,
                                                      'edgecolor': edgecolor[i % len(edgecolor)],
                                                      'lw': 5})
        radar_poly, vertices = radar_output
        axs['radar'].scatter(vertices[:, 0], vertices[:, 1],
                             c=colors[i % len(colors)], edgecolors=edgecolor[i % len(edgecolor)],
                             marker='o', s=150, zorder=2, alpha=1.0)  # Ensure alpha=1 for edges

    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=20, fontproperties=robotto_bold.prop, color='#FFFFFF')
    param_labels = radar.draw_param_labels(ax=axs['radar'], wrap=10, fontsize=20, fontproperties=robotto_bold.prop, color='#FFFFFF')

    # Display the players alternately on the left and right
    title_coords = [(0.01, 0.65), (0.99, 0.65)]
    team_coords = [(0.01, 0.25), (0.99, 0.25)]
    for i, (player, team) in enumerate(zip(players, player_teams)):
        ha = 'left' if i % 2 == 0 else 'right'
        color = colors[i % len(colors)]
        axs['title'].text(title_coords[i % 2][0], title_coords[i % 2][1] - 1 * (i // 2), f'{player}', fontsize=25,
                          fontproperties=robotto_bold.prop, ha=ha,
                          va='center', color=color)
        axs['title'].text(team_coords[i % 2][0], team_coords[i % 2][1] - 1 * (i // 2), f'{team}', fontsize=20,
                          fontproperties=robotto_bold.prop, ha=ha,
                          va='center', color=color)
        
    # Add the Twitter icon and handle
    twitter_icon_url = 'https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_%28white%29.png'
    twitter_icon = Image.open(urlopen(twitter_icon_url))

    imagebox = OffsetImage(twitter_icon, zoom=0.03)
    ab = AnnotationBbox(imagebox, (0.36, 0.67), frameon=False)
    # axs['title'].add_artist(ab)

    # axs['title'].text(0.50, 0.65, 'ALFIESCOUT', fontsize=35,
    #                   fontproperties=robotto_bold.prop,
    #                   ha='center', va='center', color='#FFFFFF')
    
    fig.set_facecolor('#070707')
    st.pyplot(fig, dpi=400)
    
    
# Function to wrap labels
def wrap_labels(labels, width):
    wrapped = []
    for label in labels:
        if label not in schemas.label_mapping().values():
            wrapped.append('\n'.join(textwrap.wrap(label, width)))
        else:
            wrapped.append(label)
    return wrapped