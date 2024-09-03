import streamlit as st
import pandas as pd
import numpy as np
from scripts import utils
from mplsoccer import FontManager
from PIL import Image
import textwrap
import matplotlib.pyplot as plt
from highlight_text import fig_text
from scipy.stats import percentileofscore
from scipy import stats

import warnings
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Futbol Paneli")

league_info_url = 'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/league_info_lookup.csv'

# Constants and Configurations
FONT_NORMAL = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf')
FONT_ITALIC = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Italic.ttf')
FONT_BOLD = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/RobotoSlab[wght].ttf')

# Abbreviated constants for English column names
COL_PLR = "Player"
COL_AGE = "Age"
COL_MCH_PLAY = "Matches played"
COL_MIN_PLAY = "Minutes played"
COL_LG = "League"
COL_SSN = "Season"
COL_POS = "Position"
COL_MAIN_POS = "Main Position"
COL_TEAM = "Team within selected timeframe"
COL_GLS = "Goals"
COL_XG = "xG"
COL_AST = "Assists"
COL_DUELS_90 = "Duels per 90"
COL_DUELS_WON = "Duels won, %"
COL_BIRTH_CTRY = "Birth country"
COL_PASS_CTRY = "Passport country"
COL_FT = "Foot"
COL_HT = "Height"
COL_WT = "Weight"
COL_ON_LOAN = "On loan"
COL_DEF_ACT_90 = "Successful defensive actions per 90"
COL_DEF_DUELS_90 = "Defensive duels per 90"
COL_DEF_DUELS_WON = "Defensive duels won, %"
COL_AIR_DUELS_90 = "Aerial duels per 90"
COL_AIR_DUELS_WON = "Aerial duels won, %"
COL_SLIDE_TKL_90 = "Sliding tackles per 90"
COL_PADJ_SLIDE = "PAdj Sliding tackles"
COL_BLKD_SHOTS_90 = "Shots blocked per 90"
COL_INT_90 = "Interceptions per 90"
COL_PADJ_INT = "PAdj Interceptions"
COL_FL_90 = "Fouls per 90"
COL_YC = "Yellow cards"
COL_YC_90 = "Yellow cards per 90"
COL_RC = "Red cards"
COL_RC_90 = "Red cards per 90"
COL_ATT_ACT_90 = "Successful attacking actions per 90"
COL_GLS_90 = "Goals per 90"
COL_NONPEN_GLS = "Non-penalty goals"
COL_NONPEN_GLS_90 = "Non-penalty goals per 90"
COL_XG_90 = "xG per 90"
COL_HEAD_GLS = "Head goals"
COL_HEAD_GLS_90 = "Head goals per 90"
COL_SHOTS = "Shots"
COL_SHOTS_90 = "Shots per 90"
COL_SHOTS_TGT = "Shots on target, %"
COL_GL_CONV = "Goal conversion, %"
COL_AST_90 = "Assists per 90"
COL_CRS_90 = "Crosses per 90"
COL_ACC_CRS = "Accurate crosses, %"
COL_L_CRS_90 = "Crosses from left flank per 90"
COL_ACC_L_CRS = "Accurate crosses from left flank, %"
COL_R_CRS_90 = "Crosses from right flank per 90"
COL_ACC_R_CRS = "Accurate crosses from right flank, %"
COL_CRS_GK_BOX_90 = "Crosses to goalie box per 90"
COL_DRIB_90 = "Dribbles per 90"
COL_SUC_DRIB = "Successful dribbles, %"
COL_OFF_DUELS_90 = "Offensive duels per 90"
COL_OFF_DUELS_WON = "Offensive duels won, %"
COL_TCH_BOX_90 = "Touches in box per 90"
COL_PROG_RUN_90 = "Progressive runs per 90"
COL_ACCEL_90 = "Accelerations per 90"
COL_REC_PASS_90 = "Received passes per 90"
COL_REC_LONG_PASS_90 = "Received long passes per 90"
COL_FLS_SUFF_90 = "Fouls suffered per 90"
COL_PASS_90 = "Passes per 90"
COL_ACC_PASS = "Accurate passes, %"
COL_FWD_PASS_90 = "Forward passes per 90"
COL_ACC_FWD_PASS = "Accurate forward passes, %"
COL_BK_PASS_90 = "Back passes per 90"
COL_ACC_BK_PASS = "Accurate back passes, %"
COL_SHT_MED_PASS_90 = "Short / medium passes per 90"
COL_ACC_SHT_MED_PASS = "Accurate short / medium passes, %"
COL_LONG_PASS_90 = "Long passes per 90"
COL_ACC_LONG_PASS = "Accurate long passes, %"
COL_AVG_PASS_LEN = "Average pass length, m"
COL_AVG_LONG_PASS_LEN = "Average long pass length, m"
COL_XA_90 = "xA per 90"
COL_SHOT_AST_90 = "Shot assists per 90"
COL_SEC_AST_90 = "Second assists per 90"
COL_THRD_AST_90 = "Third assists per 90"
COL_SMRT_PASS_90 = "Smart passes per 90"
COL_ACC_SMRT_PASS = "Accurate smart passes, %"
COL_KEY_PASS_90 = "Key passes per 90"
COL_PASS_3RD_90 = "Passes to final third per 90"
COL_ACC_PASS_3RD = "Accurate passes to final third, %"
COL_PASS_PA_90 = "Passes to penalty area per 90"
COL_ACC_PASS_PA = "Accurate passes to penalty area, %"
COL_THR_PASS_90 = "Through passes per 90"
COL_ACC_THR_PASS = "Accurate through passes, %"
COL_DEEP_COMP_90 = "Deep completions per 90"
COL_DEEP_CRS_COMP_90 = "Deep completed crosses per 90"
COL_PROG_PASS_90 = "Progressive passes per 90"
COL_ACC_PROG_PASS = "Accurate progressive passes, %"
COL_ACC_VERT_PASS = "Accurate vertical passes, %"
COL_VERT_PASS_90 = "Vertical passes per 90"
COL_CONC_GLS = "Conceded goals"
COL_CONC_GLS_90 = "Conceded goals per 90"
COL_SHOTS_AGNST = "Shots against"
COL_SHOTS_AGNST_90 = "Shots against per 90"
COL_CLEAN_SHTS = "Clean sheets"
COL_SAVE_RT = "Save rate, %"
COL_XG_AGNST = "xG against"
COL_XG_AGNST_90 = "xG against per 90"
COL_PREV_GLS = "Prevented goals"
COL_PREV_GLS_90 = "Prevented goals per 90"
COL_BK_PASS_GK_90 = "Back passes received as GK per 90"
COL_EXITS_90 = "Exits per 90"
COL_AIR_DUELS_90_1 = "Aerial duels per 90.1"
COL_FREE_KICKS_90 = "Free kicks per 90"
COL_DIR_FREE_KICKS_90 = "Direct free kicks per 90"
COL_DIR_FREE_KICKS_TGT = "Direct free kicks on target, %"
COL_CORN_90 = "Corners per 90"
COL_PEN_TAKEN = "Penalties taken"
COL_PEN_CONV = "Penalty conversion, %"
COL_PADJ_TKL_INT_90 = "pAdj Tkl+Int per 90"
COL_ASSISTS_123 = "1st, 2nd, 3rd assists"
COL_XA_SHOT_AST = "xA per Shot Assist"
COL_AIR_DUELS_WON_90 = "Aerial duels won per 90"
COL_CARDS_90 = "Cards per 90"
COL_CLEAN_SHTS_PERCENT = "Clean sheets, %"
COL_NPXG = "npxG"
COL_NPXG_90 = "npxG per 90"
COL_NPXG_SHOT = "npxG per shot"
COL_NPXGA_90 = "npxGA per 90"
COL_VERT_PASS_PERCENT = "Vertical Pass %"

# Abbreviated constants for Turkish column names
TR_OYUNCU = "Oyuncu"
TR_YAS = "Yaş"
TR_OYN_MACH = "Oynadığı maçlar"
TR_OYN_DAK = "Oynadığı dakikalar"
TR_LIG = "Lig"
TR_SEZON = "Sezon"
TR_POZ = "Pozisyon"
TR_ANA_POZ = "Ana Pozisyon"
TR_KULUP = "Kulüp"
TR_GOLLER = "Goller"
TR_XG = "Beklenen Gol (xG)"
TR_ASISTLER = "Asistler"
TR_IKILI_MUC_90 = "İkili Mücadeleler / 90"
TR_KAZ_IKILI_MUC = "Kazanılan İkili Mücadeleler %"
TR_DOGUM_ULKE = "Doğum Ülkesi"
TR_PASAPORT_ULKE = "Pasaport Ülkesi"
TR_AYAK = "Ayak"
TR_BOY = "Boy"
TR_KILO = "Kilo"
TR_KIRALIK = "Kiralık"
TR_BAS_SAV_ACT_90 = "Başarılı Savunma Eylemleri / 90"
TR_SAV_IKILI_MUC_90 = "Savunma İkili Mücadeleleri / 90"
TR_KAZ_SAV_MUC = "Kazanılan Savunma İkili Mücadeleleri %"
TR_HAVA_MUC_90 = "Hava Mücadeleleri / 90"
TR_KAZ_HAVA_MUC = "Kazanılan Hava Mücadeleleri %"
TR_TOP_CALMA_90 = "Top Çalma / 90"
TR_TOP_CALMA_PADJ = "Top Çalma (pAdj)"
TR_ENG_SHOTS_90 = "Engellenen Şutlar / 90"
TR_TOP_KESME_90 = "Top Kesme / 90"
TR_TOP_KESME_PADJ = "Top Kesme (pAdj)"
TR_FAULLER_90 = "Fauller / 90"
TR_SARI_KART = "Sarı Kartlar"
TR_SARI_KART_90 = "Sarı Kartlar / 90"
TR_KIRMIZI_KART = "Kırmızı Kartlar"
TR_KIRMIZI_KART_90 = "Kırmızı Kartlar / 90"
TR_BAS_HUC_HARE_90 = "Başarılı Hücum Hareketleri / 90"
TR_GOLLER_90 = "Goller / 90"
TR_PENAL_SIZ_GOL = "Penaltısız Goller"
TR_PENAL_SIZ_GOL_90 = "Penaltısız Goller / 90"
TR_XG_90 = "Beklenen Gol (xG) / 90"
TR_KAFA_GOLLER = "Kafa Golleri"
TR_KAFA_GOLLER_90 = "Kafa Golleri / 90"
TR_SHUTLAR = "Şutlar"
TR_SHUTLAR_90 = "Şutlar / 90"
TR_HEDEF_SHUT = "Hedefi Bulan Şutlar %"
TR_GOL_SHUT = "Gol/ Şut %"
TR_ASIST_90 = "Asist / 90"
TR_ORTALAR_90 = "Ortalar / 90"
TR_BAS_ORTA = "Başarılı Orta %"
TR_SOL_ORTA_90 = "Sol Kanattan Ortalar / 90"
TR_SOL_BAS_ORTA = "Sol Kanattan Başarılı Ortalar %"
TR_SAG_ORTA_90 = "Sağ Kanattan Ortalar / 90"
TR_SAG_BAS_ORTA = "Sağ Kanattan Başarılı Ortalar %"
TR_KALECI_KUTUSUNA_ORTALAR_90 = "Kaleci Kutusuna Ortalar / 90"
TR_DRIBBLING_90 = "Dribblingler / 90"
TR_BAS_DRIBBLING = "Başarılı Dribbling %"
TR_HUC_MUC_90 = "Hücum İkili Mücadeleleri / 90"
TR_KAZ_HUC_MUC = "Kazanılan Hücum İkili Mücadeleleri %"
TR_CEZA_DOK_90 = "Ceza Sahasında Dokunuşlar / 90"
TR_KADEMELI_TASIM_90 = "Kademeli Taşımalar / 90"
TR_HIZLANMA_90 = "Topla Hizlanmalar / 90"
TR_ALINAN_PAS_90 = "Alınan Paslar / 90"
TR_ALINAN_UZUN_PAS_90 = "Alınan Uzun Paslar / 90"
TR_KAZ_FAUL_90 = "Kazanılan Fauller / 90"
TR_PAS_90 = "Paslar / 90"
TR_BAS_PAS = "Başarılı Pas %"
TR_ILERI_PAS_90 = "İleri Paslar / 90"
TR_BAS_ILERI_PAS = "Başarılı İleri Paslar %"
TR_GERI_PAS_90 = "Geri Paslar / 90"
TR_BAS_GERI_PAS = "Başarılı Geri Paslar %"
TR_KISA_ORTA_PAS_90 = "Kısa / Orta Paslar / 90"
TR_BAS_KISA_ORTA_PAS = "Başarılı Kısa / Orta Paslar %"
TR_UZUN_PAS_90 = "Uzun Paslar / 90"
TR_BAS_UZUN_PAS = "Başarılı Uzun Paslar %"
TR_OR_ALMA_PAS_UZ = "Ortalama Pas Uzunluğu, m"
TR_OR_ALMA_UZUN_PAS_UZ = "Ortalama Uzun Pas Uzunluğu, m"
TR_BEK_ASIST_XA_90 = "Beklenen Asist (xA) / 90"
TR_SHUT_ASIST_90 = "Şut Asistleri / 90"
TR_2_ASIST_90 = "İkinci Asist / 90"
TR_3_ASIST_90 = "Üçüncü Asist / 90"
TR_AKILLI_PAS_90 = "Akıllı Paslar / 90"
TR_BAS_AKILLI_PAS = "Başarılı Akıllı Pas %"
TR_ANAHTAR_PAS_90 = "Anahtar Paslar / 90"
TR_SON_UCUNCUYE_PAS_90 = "Son Üçüncüye Paslar / 90"
TR_SON_UCUNCUYE_BAS_PAS = "Son Üçüncüye Başarılı Paslar %"
TR_CEZA_PAS_90 = "Ceza Sahasına Paslar / 90"
TR_CEZA_BAS_PAS = "Ceza Sahasına Başarılı Paslar %"
TR_ARA_PAS_90 = "Ara Paslar / 90"
TR_BAS_ARA_PAS = "Başarılı Ara Paslar %"
TR_DERIN_TAMAMLAMALAR_90 = "Derin Tamamlamalar / 90"
TR_DERIN_TAMAMLANAN_ORTALAR_90 = "Derin Tamamlanan Ortalar / 90"
TR_KADEMELI_PAS_90 = "Kademeli Paslar / 90"
TR_BAS_KADEMELI_PAS = "Başarılı Kademeli Paslar %"
TR_BAS_DIKEY_PAS = "Başarılı Dikey Paslar %"
TR_DIKEY_PAS_90 = "Dikey Paslar / 90"
TR_YENILEN_GOLLER = "Yenilen Goller"
TR_YENILEN_GOLLER_90 = "Yenilen Goller / 90"
TR_KARSI_SHUTLAR = "Karşı Şutlar"
TR_KARSI_SHUTLAR_90 = "Karşı Şutlar / 90"
TR_GOL_YEMEME = "Gol Yememe"
TR_KURTARIS_ORANI = "Kurtarış Oranı %"
TR_KARSI_BEKLENEN_GOL_XG = "Karşı Beklenen Gol (xG)"
TR_KARSI_BEKLENEN_GOL_XG_90 = "Karşı Beklenen Gol (xG) / 90"
TR_ENGELLENEN_GOLLER = "Engellenen Goller"
TR_ENGELLENEN_GOLLER_90 = "Engellenen Goller / 90"
TR_KALECIYE_GERI_PAS_90 = "Kaleciye Geri Paslar / 90"
TR_CIKISLAR_90 = "Çıkışlar / 90"
TR_HAVA_MUC_90_1 = "Hava Mücadeleleri / 90.1"
TR_SERBEST_VURUS_90 = "Serbest Vuruşlar / 90"
TR_DIREKT_SERBEST_VURUS_90 = "Direkt Serbest Vuruşlar / 90"
TR_DIREKT_SERBEST_VURUS_HEDEF = "Direkt Serbest Vuruşlar Hedef %"
TR_KORNERLER_90 = "Kornerler / 90"
TR_KULLANILAN_PENALTILAR = "Kullanılan Penaltılar"
TR_PENALTI_DONUSUMU = "Penaltı Dönüşümü %"
TR_TOP_CALMA_KESMELER_PADJ_90 = "Top Çalma & Kesmeler (pAdj) / 90"
TR_1_2_3_ASISTLER = "1., 2., 3. Asistler"
TR_XA_SUT_ASISTI = "xA başına Şut Asisti"
TR_KAZANILAN_HAVA_MUC_90 = "Kazanılan Hava Mücadeleleri / 90"
TR_KARTLAR_90 = "Kartlar / 90"
TR_GOL_YEMEME_PERCENT = "Gol Yememe %"
TR_NPXG = "npxG"
TR_NPXG_90 = "npxG / 90"
TR_NPXGA_90 = "npxGA / 90"
TR_SUT_NPXG = "Şut Başına npxG"
TR_DIKEY_PAS_PERCENT = "Dikey Pas %"

def get_column_mapping():
    return {
        COL_PLR: TR_OYUNCU,
        COL_AGE: TR_YAS,
        COL_MCH_PLAY: TR_OYN_MACH,
        COL_MIN_PLAY: TR_OYN_DAK,
        COL_LG: TR_LIG,
        COL_SSN: TR_SEZON,
        COL_POS: TR_POZ,
        COL_MAIN_POS: TR_ANA_POZ,
        COL_TEAM: TR_KULUP,
        COL_GLS: TR_GOLLER,
        COL_XG: TR_XG,
        COL_AST: TR_ASISTLER,
        COL_DUELS_90: TR_IKILI_MUC_90,
        COL_DUELS_WON: TR_KAZ_IKILI_MUC,
        COL_BIRTH_CTRY: TR_DOGUM_ULKE,
        COL_PASS_CTRY: TR_PASAPORT_ULKE,
        COL_FT: TR_AYAK,
        COL_HT: TR_BOY,
        COL_WT: TR_KILO,
        COL_ON_LOAN: TR_KIRALIK,
        COL_DEF_ACT_90: TR_BAS_SAV_ACT_90,
        COL_DEF_DUELS_90: TR_SAV_IKILI_MUC_90,
        COL_DEF_DUELS_WON: TR_KAZ_SAV_MUC,
        COL_AIR_DUELS_90: TR_HAVA_MUC_90,
        COL_AIR_DUELS_WON: TR_KAZ_HAVA_MUC,
        COL_SLIDE_TKL_90: TR_TOP_CALMA_90,
        COL_PADJ_SLIDE: TR_TOP_CALMA_PADJ,
        COL_BLKD_SHOTS_90: TR_ENG_SHOTS_90,
        COL_INT_90: TR_TOP_KESME_90,
        COL_PADJ_INT: TR_TOP_KESME_PADJ,
        COL_FL_90: TR_FAULLER_90,
        COL_YC: TR_SARI_KART,
        COL_YC_90: TR_SARI_KART_90,
        COL_RC: TR_KIRMIZI_KART,
        COL_RC_90: TR_KIRMIZI_KART_90,
        COL_ATT_ACT_90: TR_BAS_HUC_HARE_90,
        COL_GLS_90: TR_GOLLER_90,
        COL_NONPEN_GLS: TR_PENAL_SIZ_GOL,
        COL_NONPEN_GLS_90: TR_PENAL_SIZ_GOL_90,
        COL_XG_90: TR_XG_90,
        COL_HEAD_GLS: TR_KAFA_GOLLER,
        COL_HEAD_GLS_90: TR_KAFA_GOLLER_90,
        COL_SHOTS: TR_SHUTLAR,
        COL_SHOTS_90: TR_SHUTLAR_90,
        COL_SHOTS_TGT: TR_HEDEF_SHUT,
        COL_GL_CONV: TR_GOL_SHUT,
        COL_AST_90: TR_ASIST_90,
        COL_CRS_90: TR_ORTALAR_90,
        COL_ACC_CRS: TR_BAS_ORTA,
        COL_L_CRS_90: TR_SOL_ORTA_90,
        COL_ACC_L_CRS: TR_SOL_BAS_ORTA,
        COL_R_CRS_90: TR_SAG_ORTA_90,
        COL_ACC_R_CRS: TR_SAG_BAS_ORTA,
        COL_CRS_GK_BOX_90: TR_KALECI_KUTUSUNA_ORTALAR_90,
        COL_DRIB_90: TR_DRIBBLING_90,
        COL_SUC_DRIB: TR_BAS_DRIBBLING,
        COL_OFF_DUELS_90: TR_HUC_MUC_90,
        COL_OFF_DUELS_WON: TR_KAZ_HUC_MUC,
        COL_TCH_BOX_90: TR_CEZA_DOK_90,
        COL_PROG_RUN_90: TR_KADEMELI_TASIM_90,
        COL_ACCEL_90: TR_HIZLANMA_90,
        COL_REC_PASS_90: TR_ALINAN_PAS_90,
        COL_REC_LONG_PASS_90: TR_ALINAN_UZUN_PAS_90,
        COL_FLS_SUFF_90: TR_KAZ_FAUL_90,
        COL_PASS_90: TR_PAS_90,
        COL_ACC_PASS: TR_BAS_PAS,
        COL_FWD_PASS_90: TR_ILERI_PAS_90,
        COL_ACC_FWD_PASS: TR_BAS_ILERI_PAS,
        COL_BK_PASS_90: TR_GERI_PAS_90,
        COL_ACC_BK_PASS: TR_BAS_GERI_PAS,
        COL_SHT_MED_PASS_90: TR_KISA_ORTA_PAS_90,
        COL_ACC_SHT_MED_PASS: TR_BAS_KISA_ORTA_PAS,
        COL_LONG_PASS_90: TR_UZUN_PAS_90,
        COL_ACC_LONG_PASS: TR_BAS_UZUN_PAS,
        COL_AVG_PASS_LEN: TR_OR_ALMA_PAS_UZ,
        COL_AVG_LONG_PASS_LEN: TR_OR_ALMA_UZUN_PAS_UZ,
        COL_XA_90: TR_BEK_ASIST_XA_90,
        COL_SHOT_AST_90: TR_SHUT_ASIST_90,
        COL_SEC_AST_90: TR_2_ASIST_90,
        COL_THRD_AST_90: TR_3_ASIST_90,
        COL_SMRT_PASS_90: TR_AKILLI_PAS_90,
        COL_ACC_SMRT_PASS: TR_BAS_AKILLI_PAS,
        COL_KEY_PASS_90: TR_ANAHTAR_PAS_90,
        COL_PASS_3RD_90: TR_SON_UCUNCUYE_PAS_90,
        COL_ACC_PASS_3RD: TR_SON_UCUNCUYE_BAS_PAS,
        COL_PASS_PA_90: TR_CEZA_PAS_90,
        COL_ACC_PASS_PA: TR_CEZA_BAS_PAS,
        COL_THR_PASS_90: TR_ARA_PAS_90,
        COL_ACC_THR_PASS: TR_BAS_ARA_PAS,
        COL_DEEP_COMP_90: TR_DERIN_TAMAMLAMALAR_90,
        COL_DEEP_CRS_COMP_90: TR_DERIN_TAMAMLANAN_ORTALAR_90,
        COL_PROG_PASS_90: TR_KADEMELI_PAS_90,
        COL_ACC_PROG_PASS: TR_BAS_KADEMELI_PAS,
        COL_ACC_VERT_PASS: TR_BAS_DIKEY_PAS,
        COL_VERT_PASS_90: TR_DIKEY_PAS_90,
        COL_CONC_GLS: TR_YENILEN_GOLLER,
        COL_CONC_GLS_90: TR_YENILEN_GOLLER_90,
        COL_SHOTS_AGNST: TR_KARSI_SHUTLAR,
        COL_SHOTS_AGNST_90: TR_KARSI_SHUTLAR_90,
        COL_CLEAN_SHTS: TR_GOL_YEMEME,
        COL_SAVE_RT: TR_KURTARIS_ORANI,
        COL_XG_AGNST: TR_KARSI_BEKLENEN_GOL_XG,
        COL_XG_AGNST_90: TR_KARSI_BEKLENEN_GOL_XG_90,
        COL_PREV_GLS: TR_ENGELLENEN_GOLLER,
        COL_PREV_GLS_90: TR_ENGELLENEN_GOLLER_90,
        COL_BK_PASS_GK_90: TR_KALECIYE_GERI_PAS_90,
        COL_EXITS_90: TR_CIKISLAR_90,
        COL_AIR_DUELS_90_1: TR_HAVA_MUC_90_1,
        COL_FREE_KICKS_90: TR_SERBEST_VURUS_90,
        COL_DIR_FREE_KICKS_90: TR_DIREKT_SERBEST_VURUS_90,
        COL_DIR_FREE_KICKS_TGT: TR_DIREKT_SERBEST_VURUS_HEDEF,
        COL_CORN_90: TR_KORNERLER_90,
        COL_PEN_TAKEN: TR_KULLANILAN_PENALTILAR,
        COL_PEN_CONV: TR_PENALTI_DONUSUMU,
        COL_PADJ_TKL_INT_90: TR_TOP_CALMA_KESMELER_PADJ_90,
        COL_ASSISTS_123: TR_1_2_3_ASISTLER,
        COL_XA_SHOT_AST: TR_XA_SUT_ASISTI,
        COL_AIR_DUELS_WON_90: TR_KAZANILAN_HAVA_MUC_90,
        COL_CARDS_90: TR_KARTLAR_90,
        COL_CLEAN_SHTS_PERCENT: TR_GOL_YEMEME_PERCENT,
        COL_NPXG: TR_NPXG,
        COL_NPXG_90: TR_NPXG_90,
        COL_NPXG_SHOT: TR_SUT_NPXG,
        COL_NPXGA_90: TR_NPXGA_90,
        COL_VERT_PASS_PERCENT: TR_DIKEY_PAS_PERCENT
    }
    
def get_params_list():
    return [
        TR_GOLLER, TR_XG, TR_ASISTLER, TR_BEK_ASIST_XA_90, TR_IKILI_MUC_90, 
        TR_KAZ_IKILI_MUC, TR_BAS_SAV_ACT_90, TR_SAV_IKILI_MUC_90, 
        TR_KAZ_SAV_MUC, TR_HAVA_MUC_90, TR_KAZ_HAVA_MUC, TR_TOP_CALMA_90, 
        TR_TOP_CALMA_PADJ, TR_ENG_SHOTS_90, TR_TOP_KESME_90, TR_TOP_KESME_PADJ, 
        TR_FAULLER_90, TR_SARI_KART, TR_SARI_KART_90, TR_KIRMIZI_KART, 
        TR_KIRMIZI_KART_90, TR_BAS_HUC_HARE_90, TR_GOLLER_90, TR_PENAL_SIZ_GOL, 
        TR_PENAL_SIZ_GOL_90, TR_XG_90, TR_KAFA_GOLLER, TR_KAFA_GOLLER_90, 
        TR_SHUTLAR, TR_SHUTLAR_90, TR_HEDEF_SHUT, TR_GOL_SHUT, TR_ASIST_90, 
        TR_ORTALAR_90, TR_BAS_ORTA, TR_SOL_ORTA_90, TR_SOL_BAS_ORTA, 
        TR_SAG_ORTA_90, TR_SAG_BAS_ORTA, TR_KALECI_KUTUSUNA_ORTALAR_90, 
        TR_DRIBBLING_90, TR_BAS_DRIBBLING, TR_HUC_MUC_90, TR_KAZ_HUC_MUC, 
        TR_CEZA_DOK_90, TR_KADEMELI_TASIM_90, TR_HIZLANMA_90, TR_ALINAN_PAS_90, 
        TR_ALINAN_UZUN_PAS_90, TR_KAZ_FAUL_90, TR_PAS_90, TR_BAS_PAS, 
        TR_ILERI_PAS_90, TR_BAS_ILERI_PAS, TR_GERI_PAS_90, TR_BAS_GERI_PAS, 
        TR_KISA_ORTA_PAS_90, TR_BAS_KISA_ORTA_PAS, TR_UZUN_PAS_90, 
        TR_BAS_UZUN_PAS, TR_OR_ALMA_PAS_UZ, TR_OR_ALMA_UZUN_PAS_UZ, 
        TR_BEK_ASIST_XA_90, TR_SHUT_ASIST_90, TR_2_ASIST_90, TR_3_ASIST_90, 
        TR_AKILLI_PAS_90, TR_BAS_AKILLI_PAS, TR_ANAHTAR_PAS_90, 
        TR_SON_UCUNCUYE_PAS_90, TR_SON_UCUNCUYE_BAS_PAS, TR_CEZA_PAS_90, 
        TR_CEZA_BAS_PAS, TR_ARA_PAS_90, TR_BAS_ARA_PAS, TR_DERIN_TAMAMLAMALAR_90, 
        TR_DERIN_TAMAMLANAN_ORTALAR_90, TR_KADEMELI_PAS_90, TR_BAS_KADEMELI_PAS, 
        TR_BAS_DIKEY_PAS, TR_DIKEY_PAS_90, TR_YENILEN_GOLLER, TR_YENILEN_GOLLER_90, 
        TR_KARSI_SHUTLAR, TR_KARSI_SHUTLAR_90, TR_GOL_YEMEME, TR_KURTARIS_ORANI, 
        TR_KARSI_BEKLENEN_GOL_XG, TR_KARSI_BEKLENEN_GOL_XG_90, TR_ENGELLENEN_GOLLER, 
        TR_ENGELLENEN_GOLLER_90, TR_KALECIYE_GERI_PAS_90, TR_CIKISLAR_90, 
        TR_HAVA_MUC_90_1, TR_SERBEST_VURUS_90, TR_DIREKT_SERBEST_VURUS_90, 
        TR_DIREKT_SERBEST_VURUS_HEDEF, TR_KORNERLER_90, TR_KULLANILAN_PENALTILAR, 
        TR_PENALTI_DONUSUMU, TR_TOP_CALMA_KESMELER_PADJ_90, TR_1_2_3_ASISTLER, 
        TR_XA_SUT_ASISTI, TR_KAZANILAN_HAVA_MUC_90, TR_KARTLAR_90, 
        TR_GOL_YEMEME_PERCENT, TR_NPXG, TR_NPXG_90, TR_SUT_NPXG, TR_DIKEY_PAS_PERCENT
    ]

def pos_mapping(): 
    pos_mapping = {
    "Forvetler (OOS, K, SF)": "Forvet Oyuncularıyla",
    "Forvetler ve Kanatlar": "Forvet ve Kanat Oyuncularıyla",
    "Santrforsuz Forvetler (OOS, K)": "OOS ve Kanat Oyuncularıyla",
    "Kanatlar": "Kanat Oyuncularıyla",
    "Orta Saha (DOS, OS, OOS)": "Orta Saha Oyuncularıyla",
    "DOS Olmayan Orta Saha (OS, OOS)": "OS & OOS Oyuncularıyla",
    "OOS Olmayan Orta Saha (DOS, OS)": "DOS & OS Oyuncularıyla",
    "Bekler (FB/KB)": "Bek Oyuncularıyla",
    "Defansif Oyuncular (STP, FB/KB, DOS)": "Defansif Oyuncularıyla",
    "Stoper & Defansif Orta Saha": "Stoper & DOS Oyuncularıyla",
    "Santrforlar": "Santrafor Oyuncularıyla",
    "Stoperler": "Stoper Oyuncularıyla"
            }
    return pos_mapping

def get_schema_params():
    return {
        'attacking': {
            'Defending': ['Aerial duels won, %', 'pAdj Tkl+Int per 90', 'Successful defensive actions per 90'],
            'Ball Progression': ['Progressive runs per 90', 'Progressive passes per 90', 'Accelerations per 90', 'Successful dribbles, %'],
            'Attacking': ['Touches in box per 90', 'Shots per 90', 'npxG per shot', 'Goal conversion, %', 'Non-penalty goals per 90', 'npxG per 90'],
            'Chance Creation': ['Smart passes per 90', 'Second assists per 90', 'Assists per 90', 'xA per Shot Assist', 'xA per 90', 'Shot assists per 90'],
            'Accuracy': ['Accurate crosses, %', 'Accurate smart passes, %', 'Accurate long passes, %', 'Accurate short / medium passes, %']
        },
        'defensive': {
            'Defending': ['Successful defensive actions per 90', 'PAdj Sliding tackles', 'Defensive duels won, %', 'Shots blocked per 90', 'PAdj Interceptions', 'Aerial duels won per 90', 'Aerial duels won, %'],
            'Attacking': ['Accurate long passes, %', 'Crosses per 90', 'Accurate crosses, %', '1st, 2nd, 3rd assists', 'Progressive passes per 90', 'Progressive runs per 90', 'Successful dribbles, %', 'Accelerations per 90', 'xA per 90'],
            'Fouling': ['Fouls per 90', 'Cards per 90', 'Fouls suffered per 90']
        },
        'cb': {
            'Defending': ['Successful defensive actions per 90', 'PAdj Sliding tackles', 'Defensive duels won, %', 'Shots blocked per 90', 'PAdj Interceptions', 'Aerial duels won per 90', 'Aerial duels won, %'],
            'Attacking': ['Accurate long passes, %', '1st, 2nd, 3rd assists', 'Progressive passes per 90', 'Progressive runs per 90', 'Successful dribbles, %', 'Accelerations per 90', 'xA per 90'],
            'Fouling': ['Fouls per 90', 'Cards per 90', 'Fouls suffered per 90']
        },
        'general': {
            'General': ['npxG per 90', 'Non-penalty goals per 90', 'xA per 90', 'Key passes per 90', 'Through passes per 90', 'Progressive passes per 90', 'Shot assists per 90', 'Dribbles per 90', 'Touches in box per 90']
        },
        'strikers': {
            'General': ['npxG per 90', 'Non-penalty goals per 90', 'Goal conversion, %', 'xA per 90', 'Key passes per 90', 'Through passes per 90', 'Dribbles per 90', 'Touches in box per 90', 'Duels won, %', 'Aerial duels won, %', 'Received passes per 90']
        },
        'midfielders': {
            'General': ['npxGA per 90', 'Successful defensive actions per 90', 'PAdj Interceptions', 'Duels per 90', 'Duels won, %', 'Progressive runs per 90', 'Dribbles per 90', 'Forward passes per 90', 'Through passes per 90', 'Key passes per 90', 'Progressive passes per 90', 'Passes to final third per 90']
        },
        'fullbacks': {'General': ['Successful defensive actions per 90', 'PAdj Interceptions', 'Duels per 90', 'Duels won, %', 'Progressive runs per 90', 'Dribbles per 90', 'Key passes per 90', 'Crosses per 90', 'Accurate short / medium passes, %', 'xA per 90', 'Aerial duels won, %']}
    }
    
@st.cache_data
def load_lg_data(selected_league=None):
    league_data = utils.read_csv(league_info_url)
    # Apply replacements to the 'League' column
    league_data['League'] = league_data['League'].str.replace("ü", "u").replace("ó", "o").replace("ö", "o")
    leagues = league_data['League'].unique()
    if selected_league is not None:
        # Apply the replacements to the selected league if it's used for filtering
        selected_league = selected_league.replace("ü", "u").replace("ó", "o").replace("ö", "o")
        filtered_season = league_data[league_data['League'] == selected_league]['Season'].sort_values(ascending=False).unique()
        return filtered_season
    else:
        return leagues
    
@st.cache_data  
def load_season_data(selected_league, selected_season):
    full_league_name = f"{selected_league} {selected_season}"
    league_season_data = utils.read_csv2((f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{full_league_name.replace(" ","%20").replace("ü","u").replace("ó","o").replace("ö","o").replace("ã","%C3%A3")}.csv'))
    league_season_data['League'] = f'{selected_league}'
    league_season_data['Season'] = f'{selected_season}'
    league_season_data = league_season_data[list(get_column_mapping().keys())]
    return league_season_data

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

def rank_column_percentile(df, column_name):
    """
    Ranks the values in a specified column of a DataFrame based on their percentile rank.
    
    :param df: The DataFrame containing the column to be ranked.
    :param column_name: The name of the column to be ranked.
    :return: A list of percentile ranks corresponding to the values in the specified column.
    """
    return df[column_name].apply(lambda x: percentileofscore(df[column_name], x) / 100)

def get_label_mapping():
    return {
        "Kazanılan Hava Mücadeleleri %": "Kazanılan\nHava Müc.\n%",
        "Top Çalma & Kesmeler (pAdj) / 90": "Top Çalma &\nKesmeler\n(pAdj)",
        "Başarılı Savunma Eylemleri / 90": "Baş.\nSavunma\nEylemleri",
        "Kademeli Taşımalar / 90": "Kademeli\nTaşımalar",
        "Kademeli Paslar / 90": "Kademeli\nPaslar",
        "Topla Hizlanmalar / 90": "Topla\nHızlanma",
        "Başarılı Dribbling %": "Baş.\nDribbling %",
        "Ceza Sahasında Dokunuşlar / 90": "Ceza\nsahasında\ndokunuşlar",
        "Şutlar / 90": "Şutlar",
        "Şut Başına npxG": "Şut başına\nnpxG",
        "Gol/ Şut %": "Gol/\nŞut %",
        "Penaltısız Goller / 90": "Penaltısız\nGoller",
        "npxG / 90": "npxG",
        "Akıllı Paslar / 90": "Akıllı\nPaslar",
        "İkinci Asist / 90": "İkinci\nAsist",
        "Asist / 90": "Asist",
        "xA başına Şut Asisti": "xA başına\nŞut Asisti",
        "Beklenen Asist (xA) / 90": "Beklenen\nAsist (xA)",
        "Şut Asistleri / 90": "Şut\nAsist",
        "Başarılı Orta %": "Baş.\nOrta %",
        "Başarılı Akıllı Pas %": "Baş.\nAkıllı Pas\n%",
        "Başarılı Uzun Paslar %": "Baş.\nUzun Pas %",
        "Başarılı Kısa / Orta Paslar %": "Kısa ve Orta\nPas %",
        "Kazanılan Fauller / 90": "Kazanılan\nFauller",
        "Fauller / 90": "Fauller",
        "Kazanılan Hava Mücadeleleri / 90": "Kazanılan\nHava Müc.",
        "Top Kesme (pAdj)": "Top Kesme\n(pAdj)",
        "Engellenen Şutlar / 90": "Engellenen\nŞutlar",
        "Kazanılan Savunma İkili Mücadeleleri %": "Kazanılan\n(Savunma) Müc.\n%",
        "Top Çalma (pAdj)": "Top Çalma\n(pAdj)",
        "Kartlar / 90": "Kartlar",
        "Ortalar / 90": "Ortalar",
        "1., 2., 3. Asistler": "1., 2., 3.\nAsistler",
        "Kazanılan İkili Mücadeleler %": "Kazanılan\nİkili Müc. %",
        "Dribblingler / 90": "Dribblingler",
        "Ara Paslar / 90": "Ara Paslar",
        "Anahtar Paslar / 90": "Anahtar\nPaslar",
        "Aldığı paslar / 90": "Aldığı\npaslar",
        "Penaltısız xGA / 90": "Penaltısız\nxGA",
        "İkili Mücadeleler / 90": "İkili Müc.",
        "Üçüncü Bölgeye Paslar / 90": "Üçüncü\nBölgeye Paslar",
        "Başarılı İleri Paslar %": "Baş.\nİleri Paslar %",
        "İleri Paslar / 90": "İleri\nPaslar"
    }
    
# Function to wrap labels
def wrap_labels(labels, width):
    wrapped = []
    for label in labels:
        if label not in get_label_mapping().values():
            wrapped.append('\n'.join(textwrap.wrap(label, width)))
        else:
            wrapped.append(label)
    return wrapped

def scout_report(df):
    df["name"] = df["name"].replace(get_column_mapping())
    df["name"] = df["name"].replace(get_label_mapping())
    MEAN = df["mean_value"].values
    MEAN_PERCENTILE = df["mean_percentile"].values
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
    
    wrapped_labels = wrap_labels(LABELS, 10)
    
    add_labels(ANGLES[IDXS], VALUES, wrapped_labels, OFFSET, ax, text_cs, MEAN_PERCENTILE)
    
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

# def add_labels(angles, values, labels, offset, ax, text_colors):
#     padding = .05
    
#     for angle, value, label, text_col in zip(angles, values, labels, text_colors):
#         angle = angle
        
#         rotation, alignment = get_label_rotation(angle, offset)

#         ax.text(
#             x=angle, 
#             y=1.10,
#             s=label, 
#             ha=alignment, 
#             va="center", 
#             rotation=rotation,
#             color=text_col,
#         )

def add_labels(angles, values, labels, offset, ax, text_colors, mean_percentiles):
    """
    Adds labels to the radar plot and plots the mean value percentile as a dotted line.

    :param angles: List of angles where each bar is positioned.
    :param values: List of values corresponding to each bar.
    :param labels: List of metric labels for each bar.
    :param offset: The offset used for rotating text on the polar plot.
    :param ax: The matplotlib axis object where the plot is drawn.
    :param text_colors: List of colors used for the text labels.
    :param mean_percentiles: List of mean percentiles to plot as dotted lines.
    """
    padding = .05

    for i, (angle, value, label, text_col, mean_percentile) in enumerate(zip(angles, values, labels, text_colors, mean_percentiles)):
        # Obtain text rotation and alignment
        rotation, alignment = get_label_rotation(angle, offset)

        # Add the main metric label around the plot
        ax.text(
            x=angle,
            y=1.05,
            s=label,
            ha=alignment,
            va="center",
            rotation=rotation,
            color=text_col,
        )

        # Plot the mean percentile as a 3-dotted line
        ax.hlines(mean_percentile, angle - 0.055, angle + 0.055, colors='black', linestyles='dotted', linewidth=2, alpha=0.8, zorder=3)

def add_labels_dist(angles, values, labels, offset, ax, text_colors, raw_vals_full):

    # This is the space between the end of the bar and the label
    padding = .05

    # Iterate over angles, values, and labels, to add all of them.
    for i, (angle, value, label, text_col) in enumerate(zip(angles, values, labels, text_colors)):
        angle = angle
        
        # Obtain text rotation and alignment
        rotation, alignment = get_label_rotation(angle, offset)

        # And finally add the text
        ax.text(
            x=angle, 
            y=1.05,
            s=label, 
            ha=alignment, 
            va="center", 
            rotation=rotation,
            color=text_col,
        )
        
        data_to_use = raw_vals_full.iloc[:,i+1].tolist()
        mean_val = np.mean(data_to_use)
        std_dev = 0.5*np.std(data_to_use)
        mean_percentile = stats.percentileofscore(data_to_use, mean_val)
        std_dev_up_percentile = stats.percentileofscore(data_to_use, mean_val+std_dev)
        std_dev_down_percentile = stats.percentileofscore(data_to_use, mean_val-std_dev)
        
        ax.hlines(mean_percentile/100, angle - 0.055, angle + 0.055, colors='black', linestyles='dotted', linewidth=2, alpha=0.8, zorder=3)
        ax.hlines(std_dev_up_percentile/100, angle - 0.055, angle + 0.055, colors=text_col, linestyles='dotted', linewidth=2, alpha=0.8, zorder=3)
        ax.hlines(std_dev_down_percentile/100, angle - 0.055, angle + 0.055, colors=text_col, linestyles='dotted', linewidth=2, alpha=0.8, zorder=3)
        
def get_position_to_schema():
    return {
        'LCMF3': 'attacking', 'RCMF3': 'attacking', 'LAMF': 'attacking', 'LW': 'attacking',
        'RB': 'defensive', 'LB': 'defensive', 'LCMF': 'attacking', 'DMF': 'attacking',
        'RDMF': 'attacking', 'RWF': 'attacking', 'AMF': 'attacking', 'LCB': 'cb',
        'RWB': 'defensive', 'CF': 'attacking', 'LWB': 'defensive', 'GK': 'gk',
        'LDMF': 'attacking', 'RCMF': 'attacking', 'LWF': 'attacking', 'RW': 'attacking',
        'RAMF': 'attacking', 'RCB': 'cb', 'CB': 'cb', 'RCB3': 'cb', 'LCB3': 'cb',
        'RB5': 'defensive', 'RWB5': 'defensive', 'LB5': 'defensive', 'LWB5': 'defensive'
    }
             
def selected_player_data(filtered_data, comparison_data, player_name, player_age, max_age, selected_comparison, selected_schema, selected_league, selected_season, selected_position, player_image = None):
    player_data = filtered_data[
        (filtered_data['Player'] == player_name) &
        (filtered_data['Age'] == player_age)]
    player_main_position = filtered_data.loc[filtered_data['Player'] == player_name, 'Main Position'].values[0]

    # Determine schema based on player's main position
    selected_schema_type = get_position_to_schema().get(player_main_position)
    
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
            schema_to_use = get_schema_params()[selected_schema_type]
        else:
            schema_to_use = st.session_state.custom_schemas[selected_schema]
        
        # Generate radar plot
        radar_values = []
        radar_labels = []
        radar_groups = []
        radar_raw_values = []
        radar_means = []
        radar_mean_percentiles = []

        for group, metrics in schema_to_use.items():
            for metric in metrics:
                if metric in player_data.columns:
                    # Get the player's value for the metric
                    player_value = player_data.iloc[0][metric]
                    
                    # Calculate percentile rank of the player within the combined data
                    ranked_values = rank_column_percentile(combined_data, metric)
                    player_ranked_value = ranked_values[combined_data.index[combined_data['Player'] == player_name].tolist()[0]]
                    
                    # Calculate the mean value of the metric across the combined data
                    mean_value = combined_data[metric].mean()
                    
                    # Calculate the percentile of the mean value within the combined data
                    mean_percentile = stats.percentileofscore(ranked_values, mean_value)
                    
                    # Append the values for plotting
                    radar_values.append(player_ranked_value)
                    radar_labels.append(metric)
                    radar_groups.append(group)
                    radar_raw_values.append(player_value)
                    radar_means.append(mean_value)
                    radar_mean_percentiles.append(mean_percentile)

        # Create a DataFrame with the radar data and include the mean values
        radar_data = pd.DataFrame({
            'value': radar_values,                # Percentile rank of the player's value
            'name': radar_labels,                 # Metric names
            'group': radar_groups,                # Group/category of metrics
            'raw_value': radar_raw_values,        # Raw values of the player's metrics
            'mean_value': radar_means,            # Mean values of each metric
            'mean_percentile': radar_mean_percentiles  # Percentiles of mean values
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
        for position, schema in pos_mapping().items():
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
            
        fig.text(0.5175, 0.02, "@ALFIESCOUTING", ha='center', va='center', size=26, fontproperties=FONT_BOLD.prop) 
    return st.pyplot(fig, dpi=400)

position_options = [
    "Forvetler (OOS, K, SF)", "Forvetler ve Kanatlar", "Santrforsuz Forvetler (OOS, K)", "Kanatlar",
    "Orta Saha (DOS, OS, OOS)", "DOS Olmayan Orta Saha (OS, OOS)", "OOS Olmayan Orta Saha (DOS, OS)",
    "Bekler (FB/KB)", "Defansif Oyuncular (STP, FB/KB, DOS)", "Stoper & Defansif Orta Saha",
    "Santrforlar", "Stoperler"
]

##################################################################################################################################
##################################################################################################################################
##################################################################################################################################
st.title("Futbolcu Radar Oluşturma")
st.subheader("Hazırlayan @AlfieScouting, konsept @BeGriffis\nTüm veriler Wyscout'tan")
st.sidebar.header("Seçenekler")

schema_type = st.sidebar.toggle("Kendi şablonumu kullanmak istiyorum")

league_list = list(load_lg_data())
selected_league = st.sidebar.selectbox("Lig Seçiniz", league_list, index=(league_list.index("Süper Lig") if "Süper Lig" in league_list else 0))
selected_season = st.sidebar.selectbox("Sezon Seçiniz", load_lg_data(selected_league))

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
        
filtered_data, top_5_league_data = filter_data(league_season_data, selected_position, min_minutes_played, max_age)
top_5_league_data = top_5_league_data[top_5_league_data['Season']==selected_season]
renamed_data = filtered_data.rename(columns=get_column_mapping())

st.subheader(f"Data for {selected_league} - {selected_season}")
st.write(renamed_data)

st.header("Radar Oluşturma\nRadarı oluşturmak için aşağıya oyuncu adını girin (yukarıdaki tablodan kopyalayıp yapıştırabilirsiniz)")

# List of players
player_list = list(filtered_data['Player'])
player_name = st.selectbox("Futbolcu Adı", player_list)

# Filter the DataFrame to find rows with the selected player name
temp_pl_data = filtered_data[filtered_data['Player'] == player_name]

# Check how many records exist for the selected player
if len(temp_pl_data) == 1:
    # Autofill the player age if only one record exists
    player_age = temp_pl_data['Age'].values[0]
    st.write(f"Futbolcu Yaşı: {player_age}")
else:
    # If there are multiple records, show a selectbox to choose the correct age
    ages = temp_pl_data['Age'].unique()
    player_age = st.selectbox("Futbolcu Yaşı", options=ages)

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
        selected_player_data(filtered_data, comparison_data, player_name, player_age, max_age, selected_comparison, selected_schema, selected_league, selected_season, selected_position, player_image)
    except:
        st.error(f"No data found for {player_name} with age {player_age}")
