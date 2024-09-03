import streamlit as st
import pandas as pd
import numpy as np
from scripts import utils
from scripts.config_new import get_column_mapping, get_params_list
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Futbol Paneli")

st.title("Futbolcu Radar Oluşturma")
st.subheader("Hazırlayan @AlfieScouting, konsept @BeGriffis\nTüm veriler Wyscout'tan")
st.sidebar.header("Seçenekler")

schema_type = st.sidebar.toggle("Kendi şablonumu kullanmak istiyorum")

league_info_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv'

@st.cache_data
def load_lg_data(selected_league = None):
    league_data = utils.read_csv(league_info_url)
    leagues = league_data['League'].unique()
    if selected_league != None:
        filtered_season = league_data[league_data['League'] == selected_league]['Season'].sort_values(ascending=False).unique()
        return filtered_season
    else:      
        return leagues
    
league_list = list(load_lg_data())
selected_league = st.sidebar.selectbox("Lig Seçiniz", league_list, index=(league_list.index("Süper Lig") if "Süper Lig" in league_list else 0))
selected_season = st.sidebar.selectbox("Sezon Seçiniz", load_lg_data(selected_league))

@st.cache_data  
def load_season_data(selected_league, selected_season):
    full_league_name = f"{selected_league} {selected_season}"
    league_season_data = utils.read_csv2((f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{full_league_name.replace(" ","%20").replace("ü","u").replace("ó","o").replace("ö","o").replace("ã","%C3%A3")}.csv'))
    league_season_data['League'] = f'{selected_league}'
    league_season_data['Season'] = f'{selected_season}'
    league_season_data = league_season_data[list(get_column_mapping().keys())]
    return league_season_data

position_options = [
    "Forvetler (OOS, K, SF)", "Forvetler ve Kanatlar", "Santrforsuz Forvetler (OOS, K)", "Kanatlar",
    "Orta Saha (DOS, OS, OOS)", "DOS Olmayan Orta Saha (OS, OOS)", "OOS Olmayan Orta Saha (DOS, OS)",
    "Bekler (FB/KB)", "Defansif Oyuncular (STP, FB/KB, DOS)", "Stoper & Defansif Orta Saha",
    "Santrforlar", "Stoperler"
]

league_season_data = load_season_data(selected_league, selected_season)
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", position_options)
min_minutes_played = st.sidebar.number_input("Minimum Oynanan Dakikalar", value=900, min_value=0)
max_age = st.sidebar.slider("Max Yaş", min_value=15, max_value=40, value=36)

if schema_type:
    st.sidebar.header("Özel Şablon Oluşturma")
    custom_schema_name = st.sidebar.text_input("Özel Şablon Adı")
    num_groups = st.sidebar.number_input("Grup Sayısı", min_value=1, max_value=10, value=1)
    available_metrics = get_params_list()
    custom_schema = {}

    for i in range(1, num_groups + 1):
        selected_metrics = st.sidebar.multiselect(f"Grup {i} için metrikleri seçin", available_metrics)
        custom_schema[f"Group {i}"] = selected_metrics
    
    if st.sidebar.button("Özel Şablonu Kaydet"):
        if "custom_schemas" not in st.session_state:
            st.session_state.custom_schemas = {}
        st.session_state.custom_schemas[custom_schema_name] = custom_schema
        st.sidebar.success(f"Özel şablon '{custom_schema_name}' kaydedildi.", icon="✅")
        
@st.cache_data
def load_top_5_leagues(season_selection=None):
    top_5_leagues = ["La Liga", "Premier League", "Bundesliga", "Serie A", "Ligue 1"]
    if season_selection is None:
        season_selection = ["22-23", "23-24"]  # Default seasons if none are provided
    

    top_5_league_data = pd.DataFrame()
    for league in top_5_leagues:
        for season in season_selection:
            league_file = f"{league} {season}.csv".replace(" ", "%20").replace("ü", "u").replace("ó", "o").replace("ö", "o").replace("ã", "a")
            league_data = utils.read_csv2(f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{league_file}')
            league_data['League'] = league
            league_data['Season'] = season
            league_data = league_data[list(get_column_mapping().keys())]
            top_5_league_data = pd.concat([top_5_league_data, league_data], ignore_index=True)
    return top_5_league_data

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

filtered_data, top_5_league_data = filter_data(league_season_data, selected_position, min_minutes_played, max_age, selected_season)
renamed_data = filtered_data.rename(columns=get_column_mapping())

st.subheader(f"Data for {selected_league} - {selected_season}")
st.write(renamed_data)

st.header("Radar Oluşturma\nRadarı oluşturmak için aşağıya oyuncu adını girin (yukarıdaki tablodan kopyalayıp yapıştırabilirsiniz)")

player_list = list(filtered_data['Player'])
player_name = st.selectbox("Futbolcu Adı", player_list)
player_age = st.number_input("Futbolcu Yaşı", max_value=45)

if schema_type:
    schema_options = ["Default Schema"]
    if "custom_schemas" in st.session_state:
        schema_options += list(st.session_state.custom_schemas.keys())
    selected_schema = st.selectbox("Şablon Seçin", schema_options)
else:
    selected_schema = "Default Schema"

crop_url = 'https://crop-circle.imageonline.co/'
st.markdown("Eğer resim eklemek istiyorsanız, orijinal resmi [https://crop-circle.imageonline.co/](%s) adresine yükleyerek dönüştürün." % crop_url)
player_image = st.file_uploader("Futbolcunun Resmini Yükle", type=["png", "jpg", "jpeg"])

comparison_options = ["Top 5 Ligi", "Kendi Ligi"]
selected_comparison = st.selectbox("Karşılaştırma", comparison_options)

if selected_comparison == "Top 5 Ligi":
    comparison_data = top_5_league_data
else:
    comparison_data = filtered_data

if st.button("Radar Oluştur"):
    try:
        utils.selected_player_data(filtered_data, comparison_data, player_name, player_age, max_age, selected_comparison, selected_schema, selected_league, selected_season, selected_position, player_image)
    except:
        st.error(f"No data found for {player_name} with age {player_age}")                                                                                                                                                   