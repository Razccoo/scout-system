import streamlit as st
import pandas
import numpy
from scripts import schemas, utils

crop_url = 'https://crop-circle.imageonline.co/'

st.set_page_config(page_title="Radar Chart", page_icon="📈")

st.title("Futbolcu Radar Oluşturma")
st.subheader("Tüm veriler Wyscout'tan")
st.subheader('Hazırlayan @AlfieScouting, konsept @BeGriffis')
st.sidebar.header("Seçenekler")

schema_type = st.sidebar.toggle("Kendi şablonumu kullanmak istiyorum")

selected_league = st.sidebar.selectbox("Lig Seçiniz", utils.load_lg_data())
selected_season = st.sidebar.selectbox("Sezon Seçiniz", utils.load_lg_data(selected_league))

league_season_data = utils.load_player_data(selected_league, selected_season)
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", schemas.position_options)
min_minutes_played = st.sidebar.number_input("Minimum Oynanan Dakikalar", value=900, min_value=0)
max_age = st.sidebar.slider("Max Yaş", min_value=16, max_value=45, value=45)

if schema_type:
    st.sidebar.header("Özel Şablon Oluşturma")
    custom_schema_name = st.sidebar.text_input("Özel Şablon Adı")
    num_groups = st.sidebar.number_input("Grup Sayısı", min_value=1, max_value=10, value=1)
    available_metrics = schemas.params_list()
    custom_schema = {}

    for i in range(1, num_groups + 1):
        selected_metrics = st.sidebar.multiselect(f"Grup {i} için metrikleri seçin", available_metrics)
        custom_schema[f"Group {i}"] = selected_metrics
    
    if st.sidebar.button("Özel Şablonu Kaydet"):
        if "custom_schemas" not in st.session_state:
            st.session_state.custom_schemas = {}
        st.session_state.custom_schemas[custom_schema_name] = custom_schema
        st.sidebar.success(f"Özel şablon '{custom_schema_name}' kaydedildi.", icon="✅")

filtered_data, top_5_league_data = utils.filter_data(league_season_data, selected_position, min_minutes_played, max_age)

st.subheader(f"Data for {selected_league} - {selected_season}")
st.write(filtered_data)

st.header("Futbolcu Radarı Oluşturma\nRadarı oluşturmak için aşağıya oyuncu adını girin (yukarıdaki tablodan kopyalayıp yapıştırabilirsiniz)")
player_name = st.text_input("Futbolcu Adı")
player_age = st.number_input("Futbolcu Yaşı", max_value=45)
# Schema selector
if schema_type:
    schema_options = ["Default Schema"]
    if "custom_schemas" in st.session_state:
        schema_options += list(st.session_state.custom_schemas.keys())
    selected_schema = st.selectbox("Şablon Seçin", schema_options)
else:
    selected_schema = "Default Schema"

# Image uploader for player's image
st.markdown("Eğer resim eklemek istiyorsanız, orijinal resmi [https://crop-circle.imageonline.co/](%s) adresine yükleyerek dönüştürün." % crop_url)
player_image = st.file_uploader("Futbolcunun Resmini Yükle", type=["png", "jpg", "jpeg"])

# Add option to compare player's metrics
comparison_options = ["Top 5 Ligi", "Kendi Ligi"]
selected_comparison = st.selectbox("Karşılaştırma", comparison_options)
# Load the top 5 leagues data if needed
if selected_comparison == "Top 5 Ligi":
    comparison_data = top_5_league_data
else:
    comparison_data = filtered_data

if st.button("Radar Oluştur"):
    try:
        utils.selected_player_data(filtered_data, comparison_data, player_name, player_age, max_age, selected_comparison, selected_schema, selected_league, selected_season, player_image)
    except:
        st.error(f"No data found for {player_name} with age {player_age}")