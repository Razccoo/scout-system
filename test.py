import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import FontManager
from PIL import Image
import urllib.parse
from scipy import stats
import textwrap
from highlight_text import fig_text
import json

font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                        'src/hinted/Roboto-Regular.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                        'src/hinted/Roboto-Italic.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab[wght].ttf')
# URL for the league information CSV
league_info_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv'
crop_url = 'https://crop-circle.imageonline.co/'

schema_params = {
    "Defending": ["Aerial duels won, %", "pAdj Tkl+Int per 90", "Successful defensive actions per 90"],
    "Ball Progression": ["Progressive runs per 90", "Progressive passes per 90", "Accelerations per 90", "Successful dribbles, %"],
    "Attacking": ["Touches in box per 90", "Shots per 90", "npxG per shot", "Goal conversion, %", "Non-penalty goals per 90", "npxG per 90"],
    "Chance Creation": ["Smart passes per 90", "Second assists per 90", "Assists per 90", "xA per Shot Assist", "xA per 90", "Shot assists per 90"],
    "Accuracy": ["Accurate crosses, %", "Accurate smart passes, %", "Accurate long passes, %", "Accurate short / medium passes, %"]
}

wingers_params = {
    "Vision": ["Smart passes per 90", "Key passes per 90", "xA per 90", "Shot assists per 90", "Second assists per 90", "Deep completions per 90"],
    "Passing": ["Vertical Pass %", "Short / medium passes per 90", "Accurate short / medium passes, %", "Long passes per 90", "Accurate long passes, %", "Crosses per 90", "Accurate crosses, %"],
    "Quality Final Action": ["Goal conversion, %", "npxG per shot", "Non-penalty goals per 90", "Shots on target, %", "Assists per 90"],
    "Aggression": ["pAdj Tkl+Int per 90", "Fouls per 90", "Duels per 90", "Aerial duels won, %", "Duels won, %"],
    "Build-Up": ["Accelerations per 90", "Progressive runs per 90", "Progressive passes per 90", "Dribbles per 90", "Successful dribbles, %"]
}

label_mapping = {
    "Aerial duels won, %": "Aerial\nWin %",
    "pAdj Tkl+Int per 90": "Tackles &\nInt (pAdj)",
    "Successful defensive actions per 90": "Defensive\nActions",
    "Progressive runs per 90": "Prog.\nCarries",
    "Progressive passes per 90": "Prog.\nPasses",
    "Accelerations per 90": "Acceleration\nwith Ball",
    "Successful dribbles, %": "Dribble\nSuccess %",
    "Touches in box per 90": "Touches in\nPen Box",
    "Shots per 90": "Shots",
    "npxG per shot": "npxG\nper Shot",
    "Goal conversion, %": "Goals/Shot\non Target %",
    "Non-penalty goals per 90": "Non-Pen\nGoals",
    "npxG per 90": "npxG",
    "Smart passes per 90": "Smart\nPasses",
    "Second assists per 90": "Second\nAssists",
    "Assists per 90": "Assists",
    "xA per Shot Assist": "xA per\nShot Assist",
    "xA per 90": "Expected\nAssists (xA)",
    "Shot assists per 90": "Shot\nAssists",
    "Accurate crosses, %": "Cross\nCompletion %",
    "Accurate smart passes, %": "Smart\nPass %",
    "Accurate long passes, %": "Long\nPass %",
    "Accurate short / medium passes, %": "Short &\nMed Pass %"
}

def rename_columns(df, mapping):
    return df.rename(columns=mapping)

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
    return df

def rank_column(df, column_name):
    return stats.rankdata(df[column_name], "average") / len(df[column_name])

def get_label_rotation(angle, offset):
    rotation = np.rad2deg(angle + offset) + 90
    if angle <= np.pi / 2:
        alignment = "center"
        rotation = rotation + 180
    elif 4.3 < angle < np.pi * 2:
        alignment = "center"
        rotation = rotation - 180
    else: 
        alignment = "center"
    return rotation, alignment

def add_labels(angles, values, labels, offset, ax, text_colors):
    padding = .10
    
    for angle, value, label, text_col in zip(angles, values, labels, text_colors):
        angle = angle
        
        rotation, alignment = get_label_rotation(angle, offset)

        ax.text(
            x=angle, 
            y=1.05,
            s=label, 
            ha=alignment, 
            va="center", 
            rotation=rotation,
            color=text_col,
        )

def scout_report(df):
    df["name"] = df["name"].replace(label_mapping)
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
        ax.plot(x2, [1] * 50, color="#bebebe", lw=0.8)

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
            if label not in label_mapping.values():
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

def filter_by_position(df, position):
    fw = ["CF", "RW", "LW", "AMF"]
    if position == "Forwards (AM, W, CF)":
        return df[df['Main Position'].str.contains('|'.join(fw), na=False)]
    
    stw = ["CF", "RW", "LW", "LAMF", "RAMF"]
    if position == "Strikers and Wingers":
        return df[df['Main Position'].str.contains('|'.join(stw), na=False)]
    
    fwns = ["RW", "LW", "AMF"]
    if position == "Forwards no ST (AM, W)":
        return df[df['Main Position'].str.contains('|'.join(fwns), na=False)]
    
    wing = ["RW", "LW", "WF", "LAMF", "RAMF"]
    if position == "Wingers":
        return df[df['Main Position'].str.contains('|'.join(wing), na=False)]

    mids = ["DMF", "CMF", "AMF"]
    if position == "Central Midfielders (DM, CM, CAM)":
        return df[df['Main Position'].str.contains('|'.join(mids), na=False)]

    cms = ["CMF", "AMF"]
    if position == "Central Midfielders no DM (CM, CAM)":
        return df[df['Main Position'].str.contains('|'.join(cms), na=False)]

    dms = ["CMF", "DMF"]
    if position == "Central Midfielders no CAM (DM, CM)":
        return df[df['Main Position'].str.contains('|'.join(dms), na=False)]

    fbs = ["LB", "RB", "WB"]
    if position == "Fullbacks (FBs/WBs)":
        return df[df['Main Position'].str.contains('|'.join(fbs), na=False)]

    defs = ["LB", "RB", "WB", "CB", "DMF"]
    if position == "Defenders (CB, FB/WB, DM)":
        return df[df['Main Position'].str.contains('|'.join(defs), na=False)]

    cbdm = ["CB", "DMF"]
    if position == "CBs & DMs":
        return df[df['Main Position'].str.contains('|'.join(cbdm), na=False)]

    cf = ["CF"]
    if position == "Strikers":
        return df[df['Main Position'].str.contains('|'.join(cf), na=False)]

    cb = ["CB"]
    if position == "Centre-Backs":
        return df[df['Main Position'].str.contains('|'.join(cb), na=False)]
    else:
        return df

# Function to load data for the Top 5 Leagues
def load_top_5_leagues():
    top_5_leagues = ["La Liga 23-24", "Premier League 23-24", "Bundesliga 23-24", "Serie A 23-24", "Ligue 1 23-24"]
    top_5_league_data = []
    for league in top_5_leagues:
        league_data = read_csv2((f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{league.replace(" ","%20").replace("ü","u").replace("ó","o").replace("ö","o")}.csv'))
        top_5_league_data.append(league_data)
    return pd.concat(top_5_league_data, ignore_index=True)

#####################################################################################################################################
#####################################################################################################################################

def main():
    st.title("Futbol Yetenek Araştırması & Radar Oluşturma")
    st.subheader("Tüm veriler Wyscout'tan")
    st.subheader('Hazırlayan @AlfieScouting, Konsept @BeGriffis')
    st.sidebar.header("Seçenekler")
    
    # Selection box for schema type at the top of the sidebar
    schema_type = st.sidebar.toggle("Kendi şablonumu kullanmak istiyorum")
    
    # Load league information
    league_data = read_csv(league_info_url)
    leagues = league_data['League'].unique()
    
    # League selector
    selected_league = st.sidebar.selectbox("Lig Seçiniz", leagues)
    
    # Filter seasons based on the selected league
    filtered_seasons = league_data[league_data['League'] == selected_league]['Season'].unique()
    
    # Season selector
    selected_season = st.sidebar.selectbox("Sezon Seçiniz", filtered_seasons)
    
    full_league_name = f"{selected_league} {selected_season}"
    
    # Load the league data from the constructed URL
    try:
        league_season_data = read_csv2((f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{full_league_name.replace(" ","%20").replace("ü","u").replace("ó","o").replace("ö","o")}.csv'))
        league_season_data['League'] = f'{selected_league}'
        
        # Primary Position selector
        position_options = [
            "Forwards (AM, W, CF)", "Strikers and Wingers", "Forwards no ST (AM, W)", 
            "Wingers", "Central Midfielders (DM, CM, CAM)", "Central Midfielders no DM (CM, CAM)",
            "Central Midfielders no CAM (DM, CM)", "Fullbacks (FBs/WBs)", 
            "Defenders (CB, FB/WB, DM)", "CBs & DMs", "Strikers", "Centre-Backs"
        ]
        selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", position_options)
        
        # Minimum Minutes Played input
        min_minutes_played = st.sidebar.number_input("Minimum Oynanan Dakikalar", value=900, min_value=0)
        
        # Max Age slider
        max_age = st.sidebar.slider("Max Age", min_value=16, max_value=45, value=25)
        
        # Add option to compare player's metrics
        comparison_options = ["Kendi Ligi", "Top 5 Ligi"]
        selected_comparison = st.sidebar.selectbox("Karşılaştırma", comparison_options)

        # Show custom schema inputs only if "Create Custom Schema" is selected
        if schema_type:
            st.sidebar.header("Özel Şablon Oluşturma")
            custom_schema_name = st.sidebar.text_input("Özel Şablon Adı")
            num_groups = st.sidebar.number_input("Grup Sayısı", min_value=1, max_value=10, value=1)
            
            available_metrics = list(league_season_data.columns)
            custom_schema = {}
            
            for i in range(1, num_groups + 1):
                selected_metrics = st.sidebar.multiselect(f"Grup {i} için metrikleri seçin", available_metrics)
                custom_schema[f"Group {i}"] = selected_metrics
            
            if st.sidebar.button("Özel Şablonu Kaydet"):
                if "custom_schemas" not in st.session_state:
                    st.session_state.custom_schemas = {}
                st.session_state.custom_schemas[custom_schema_name] = custom_schema
                st.sidebar.success(f"Özel şablon '{custom_schema_name}' kaydedildi.", icon="✅")

        # Filter the data based on the selected filters
        filtered_data = filter_by_position(league_season_data, selected_position)
        filtered_data = filtered_data[
            (filtered_data['Minutes played'] >= min_minutes_played) &
            (filtered_data['Age'] <= max_age)
        ].reset_index(drop=True)
        
        # Load the top 5 leagues data if needed
        if selected_comparison == "Top 5 Ligi":
            top_5_league_data = filter_by_position(load_top_5_leagues(), selected_position)
            comparison_data = top_5_league_data[
                (top_5_league_data['Minutes played'] >= min_minutes_played) &
                (top_5_league_data['Age'] <= max_age)
            ].reset_index(drop=True)
        else:
            comparison_data = filtered_data

        st.subheader(f"Data for {selected_league} - {selected_season}")
        st.write(filtered_data)
        
        # Inputs for player's radar
        st.header("Futbolcu Radarı Oluşturma")
        player_name = st.text_input("Futbolcu Adı")
        player_age = st.number_input("Futbolcu Yaşı", max_value=45, value=0)
        
        # Schema selector
        schema_options = ["Default Schema"]
        if "custom_schemas" in st.session_state:
            schema_options += list(st.session_state.custom_schemas.keys())
        selected_schema = st.selectbox("Şablon Seçin", schema_options)
        
        # Image uploader for player's image
        st.markdown("Eğer resim eklemek istiyorsanız, orijinal resmi [https://crop-circle.imageonline.co/](%s) adresine yükleyerek dönüştürün." % crop_url)
        player_image = st.file_uploader("Futbolcunun Resmini Yükle", type=["png", "jpg", "jpeg"])
        
        if st.button("Radar Oluştur"):
            player_data = filtered_data[
                (filtered_data['Player'] == player_name) &
                (filtered_data['Age'] == player_age)
            ]
            
            # Initialize combined_data
            combined_data = pd.DataFrame()
        
            # Check if the player is already playing in the top 5 leagues
            player_in_top_5 = any(player_data['League'].isin(["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1"]))
        
            if selected_comparison == "Top 5 Ligi":
                if player_in_top_5:
                    # Player is already in the top 5 leagues, use filtered data
                    player_data = filtered_data[
                        (filtered_data['Player'] == player_name) &
                        (filtered_data['Age'] == player_age)
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
            
            player_pos = player_data['Main Position'].iloc[0]
            player_min = player_data['Minutes played'].iloc[0]
            player_team = player_data['Team within selected timeframe'].iloc[0]
            title_note = " 90 Dk Başına"
            
            if not player_data.empty:
                st.subheader(f"Data for {player_name} (Age {player_age})")
                st.write(player_data)
                
                # Use selected schema
                if selected_schema == "Default Schema":
                    schema_to_use = schema_params
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
                
                if player_image is not None:
                    image = Image.open(player_image)
                    newax = fig.add_axes([.425, .405, 0.18, 0.18], anchor='C', zorder=1)
                    newax.imshow(image)
                    newax.axis('off')
                
                plt.suptitle(f'{player_name} ({player_age}, {player_pos}, {player_min} mins.), {player_team}\n{selected_season} {selected_league} Yüzdelik Sıralamalar{title_note}',
                            fontsize=17,
                            fontfamily="DejaVu Sans",
                            color="#4A2E19", #4A2E19
                            fontweight="bold", fontname="DejaVu Sans",
                            x=0.5,
                            y=.97)
                
                fig.text(0.10, 0.02, "@ALFIESCOUTING", ha='left', va='center', size=30, fontproperties=font_bold.prop,) 
    
                st.pyplot(fig)
                radar_data
            else:
                st.error(f"No data found for {player_name} with age {player_age}")
    
    except Exception as e:
        st.error(f"Could not load data for {selected_league} - {selected_season}. Error: {e}")

if __name__ == "__main__":
    main()
