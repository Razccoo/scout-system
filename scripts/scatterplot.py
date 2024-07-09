# scatterplot.py
import streamlit as st
import matplotlib
import plotly.express as px
from scripts import utils

param_list = [
            'Yaş', 'Oynadığı maçlar', 'Goller', 'Beklenen Gol (xG)', 'Asistler', 'Beklenen Asist (xA)', 'İkili Mücadeleler / 90', 'Kazanılan İkili Mücadeleler %', 'Başarılı Savunma Eylemleri / 90',
            'Savunma İkili Mücadeleleri / 90', 'Kazanılan Savunma İkili Mücadeleleri %', 'Hava Mücadeleleri / 90', 'Kazanılan Hava Mücadeleleri %', 'Top Çalma / 90',
            'Top Çalma (pAdj)', 'Engellenen Şutlar / 90', 'Top Kesme / 90', 'Top Kesme (pAdj)', 'Fauller / 90', 'Sarı Kartlar', 'Sarı Kartlar / 90', 'Kırmızı Kartlar',
            'Kırmızı Kartlar / 90', 'Başarılı Hücum Hareketleri / 90', 'Goller / 90', 'Penaltısız Goller', 'Penaltısız Goller / 90', 'Beklenen Gol (xG) / 90',
            'Kafa Golleri', 'Kafa Golleri / 90', 'Şutlar', 'Şutlar / 90', 'Hedefi Bulan Şutlar %', 'Gol/ Şut %', 'Asist / 90', 'Ortalar / 90', 'Başarılı Orta %', 'Sol Kanattan Ortalar / 90',
            'Sol Kanattan Başarılı Ortalar %', 'Sağ Kanattan Ortalar / 90', 'Sağ Kanattan Başarılı Ortalar %', 'Kaleci Kutusuna Ortalar / 90', 'Dribblingler / 90',
            'Başarılı Dribbling %', 'Hücum İkili Mücadeleleri / 90', 'Kazanılan Hücum İkili Mücadeleleri %', 'Ceza Sahasında Dokunuşlar / 90', 'Kademeli Taşımalar / 90',
            'Topla Hizlanmalar / 90', 'Alınan Paslar / 90', 'Alınan Uzun Paslar / 90', 'Kazanılan Fauller / 90', 'Paslar / 90', 'Başarılı Pas %', 'İleri Paslar / 90', 'Başarılı İleri Paslar %',
            'Geri Paslar / 90', 'Başarılı Geri Paslar %', 'Kısa / Orta Paslar / 90', 'Başarılı Kısa / Orta Paslar %', 'Uzun Paslar / 90', 'Başarılı Uzun Paslar %', 'Ortalama Pas Uzunluğu, m',
            'Ortalama Uzun Pas Uzunluğu, m', 'Beklenen Asist (xA) / 90', 'Şut Asistleri / 90', 'İkinci Asist / 90', 'Üçüncü Asist / 90', 'Akıllı Paslar / 90',
            'Başarılı Akıllı Pas %', 'Anahtar Paslar / 90', 'Son Üçüncüye Paslar / 90', 'Son Üçüncüye Başarılı Paslar %', 'Ceza Sahasına Paslar / 90',
            'Ceza Sahasına Başarılı Paslar %', 'Ara Paslar / 90', 'Başarılı Ara Paslar %', 'Derin Tamamlamalar / 90', 'Derin Tamamlanan Ortalar / 90',
            'Kademeli Paslar / 90', 'Başarılı Kademeli Paslar %', 'Başarılı Dikey Paslar %', 'Dikey Paslar / 90', 'Yenilen Goller', 'Yenilen Goller / 90',
            'Karşı Şutlar', 'Karşı Şutlar / 90', 'Gol Yememe', 'Kurtarış Oranı %', 'Karşı Beklenen Gol (xG)', 'Karşı Beklenen Gol (xG) / 90', 'Engellenen Goller',
            'Engellenen Goller / 90', 'Kaleciye Geri Paslar / 90', 'Çıkışlar / 90', 'Hava Mücadeleleri / 90.1', 'Serbest Vuruşlar / 90', 'Direkt Serbest Vuruşlar / 90',
            'Direkt Serbest Vuruşlar Hedef %', 'Kornerler / 90', 'Kullanılan Penaltılar', 'Penaltı Dönüşümü %', 'Top Çalma & Kesmeler (pAdj) / 90', '1., 2., 3. Asistler',
            'xA başına Şut Asisti', 'Kazanılan Hava Mücadeleleri / 90', 'Kartlar / 90', 'Gol Yememe %', 'npxG', 'npxG / 90', 'Şut Başına npxG', 'Dikey Pas %'
            ]

def pointcolor():
    options = param_list
    # point_color = st.sidebar.selectbox("Nokta Renk Değişkeni", options, index=default_index)
    return options

def colorscale():
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    colorscales = px.colors.named_colorscales()
    return colorscales

def filter_data(selected_league, selected_season, selected_position, min_minutes_played):
    top_5_league_data = utils.filter_by_position(utils.load_top_5_leagues(), selected_position)
    top_5_league_data = top_5_league_data[
        (top_5_league_data['Oynadığı dakikalar'] >= min_minutes_played)
    ].reset_index(drop=True)

    filtered_data = utils.filter_by_position(utils.load_player_data(selected_league, selected_season), selected_position)
    filtered_data = filtered_data[
        (filtered_data['Oynadığı dakikalar'] >= min_minutes_played)
    ].reset_index(drop=True)
    return filtered_data, top_5_league_data