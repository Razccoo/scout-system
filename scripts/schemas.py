# mappingdict.py


def position_to_schema():
    position_to_schema = {
        'LCMF3': 'attacking', 'RCMF3': 'attacking', 'LAMF': 'attacking', 'LW': 'attacking',
                'RB': 'defensive', 'LB': 'defensive', 'LCMF': 'attacking', 'DMF': 'attacking',
                'RDMF': 'attacking', 'RWF': 'attacking', 'AMF': 'attacking', 'LCB': 'cb',
                'RWB': 'defensive', 'CF': 'attacking', 'LWB': 'defensive', 'GK': 'gk',
                'LDMF': 'attacking', 'RCMF': 'attacking', 'LWF': 'attacking', 'RW': 'attacking',
                'RAMF': 'attacking', 'RCB': 'cb', 'CB': 'cb', 'RCB3': 'cb',
                'LCB3': 'cb', 'RB5': 'defensive', 'RWB5': 'defensive', 'LB5': 'defensive',
                'LWB5': 'defensive'
    }
    return position_to_schema

def params_list():
    param_list = [
        'Goller', 'Beklenen Gol (xG)', 'Asistler', 'Beklenen Asist (xA)', 'İkili Mücadeleler / 90', 'Kazanılan İkili Mücadeleler %', 'Savunma Eylemleri / 90', 'Başarılı Savunma Eylemleri / 90'
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
    return param_list

def schema_params():
    schema_params = {
                "attacking": {
                    "Defending": ["Kazanılan Hava Mücadeleleri %", "Top Çalma & Kesmeler (pAdj) / 90", "Başarılı Savunma Eylemleri / 90"],
                    "Ball Progression": ["Kademeli Taşımalar / 90", "Kademeli Paslar / 90", "Topla Hizlanmalar / 90", "Başarılı Dribbling %"],
                    "Attacking": ["Ceza Sahasında Dokunuşlar / 90", "Şutlar / 90", "Şut Başına npxG", "Gol/ Şut %", "Penaltısız Goller / 90", "npxG / 90"],
                    "Chance Creation": ["Akıllı Paslar / 90", "İkinci Asist / 90", "Asist / 90", "xA başına Şut Asisti", "Beklenen Asist (xA) / 90", "Şut Asistleri / 90"],
                    "Accuracy": ["Başarılı Orta %", "Başarılı Akıllı Pas %", "Başarılı Uzun Paslar %", "Başarılı Kısa / Orta Paslar %"]
                },
                "defensive": {
                    "Defending": [
                        "Başarılı Savunma Eylemleri / 90", "Top Çalma (pAdj)", "Kazanılan Savunma İkili Mücadeleleri %", 
                        "Engellenen Şutlar / 90", "Top Kesme (pAdj)", "Kazanılan Hava Mücadeleleri / 90", 
                        "Kazanılan Hava Mücadeleleri %"
                    ],
                    "Attacking": [
                        "Başarılı Uzun Paslar %", "Ortalar / 90", "Başarılı Orta %", 
                        "1., 2., 3. Asistler", "Kademeli Paslar / 90", "Kademeli Taşımalar / 90", 
                        "Başarılı Dribbling %", "Topla Hizlanmalar / 90", "Beklenen Asist (xA) / 90"
                    ],
                    "Fouling": [
                        "Fauller / 90", "Kartlar / 90", "Kazanılan Fauller / 90"
                    ]
                },
                "cb": {
                    "Defending": [
                        "Başarılı Savunma Eylemleri / 90", "Top Çalma (pAdj)", "Kazanılan Savunma İkili Mücadeleleri %", 
                        "Engellenen Şutlar / 90", "Top Kesme (pAdj)", "Kazanılan Hava Mücadeleleri / 90", 
                        "Kazanılan Hava Mücadeleleri %"
                    ],
                    "Attacking": [
                        "Başarılı Uzun Paslar %", "1., 2., 3. Asistler", "Kademeli Paslar / 90", "Kademeli Taşımalar / 90", 
                        "Başarılı Dribbling %", "Topla Hizlanmalar / 90", "Beklenen Asist (xA) / 90"
                    ],
                    "Fouling": [
                        "Fauller / 90", "Kartlar / 90", "Kazanılan Fauller / 90"
                    ]
                }
    }
    return schema_params

def wingers_params():
    wingers_params = {
                "Vision": ["Smart passes per 90", "Key passes per 90", "xA per 90", "Shot assists per 90", "Second assists per 90", "Deep completions per 90"],
                "Passing": ["Vertical Pass %", "Short / medium passes per 90", "Accurate short / medium passes, %", "Long passes per 90", "Accurate long passes, %", "Crosses per 90", "Accurate crosses, %"],
                "Quality Final Action": ["Goal conversion, %", "npxG per shot", "Non-penalty goals per 90", "Shots on target, %", "Assists per 90"],
                "Aggression": ["pAdj Tkl+Int per 90", "Fouls per 90", "Duels per 90", "Aerial duels won, %", "Duels won, %"],
                "Build-Up": ["Accelerations per 90", "Progressive runs per 90", "Progressive passes per 90", "Dribbles per 90", "Successful dribbles, %"]
    }
    return wingers_params

def label_mapping():
    label_mapping = {
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
                "1., 2., 3. Asistler": "1., 2., 3.\nAsistler"
    }
    return label_mapping

def column_mapping():
    column_mapping = {
        "Player": "Oyuncu", "Age": "Yaş", "Minutes played": "Oynadığı dakikalar", # "League": "Lig", "Position": "Pozisyon",
        "Ana Pozisyon": "Ana Pozisyon", "Team within selected timeframe": "Kulüp", "Goals": "Goller", "xG": "Beklenen Gol (xG)",
        "Assists": "Asistler", "xA": "Beklenen Asist (xA)", "Duels per 90": "İkili Mücadeleler / 90", "Duels won, %": "Kazanılan İkili Mücadeleler %",
        "Birth country": "Doğum Ülkesi", "Passport country": "Pasaport Ülkesi", "Foot": "Ayak", "Height": "Boy", "Weight": "Kilo",
        "On loan": "Kiralık", "Successful defensive actions per 90": "Başarılı Savunma Eylemleri / 90", "Defensive duels per 90": "Savunma İkili Mücadeleleri / 90",
        "Defensive duels won, %": "Kazanılan Savunma İkili Mücadeleleri %", "Aerial duels per 90": "Hava Mücadeleleri / 90", "Aerial duels won, %": "Kazanılan Hava Mücadeleleri %",
        "Sliding tackles per 90": "Top Çalma  / 90", "PAdj Sliding tackles": "Top Çalma (pAdj)", "Shots blocked per 90": "Engellenen Şutlar / 90",
        "Interceptions per 90": "Top Kesme / 90", "PAdj Interceptions": "Top Kesme (pAdj)", "Fouls per 90": "Fauller / 90",
        "Yellow cards": "Sarı Kartlar", "Yellow cards per 90": "Sarı Kartlar / 90", "Red cards": "Kırmızı Kartlar", "Red cards per 90": "Kırmızı Kartlar / 90",
        "Successful attacking actions per 90": "Başarılı Hücum Hareketleri / 90", "Goals per 90": "Goller / 90", "Non-penalty goals": "Penaltısız Goller",
        "Non-penalty goals per 90": "Penaltısız Goller / 90", "xG per 90": "Beklenen Gol (xG) / 90",
        "Head goals": "Kafa Golleri", "Head goals per 90": "Kafa Golleri / 90", "Shots": "Şutlar", "Shots per 90": "Şutlar / 90", "Shots on target, %": "Hedefi Bulan Şutlar %",
        "Goal conversion, %": "Gol/ Şut %", "Assists per 90": "Asist / 90", "Crosses per 90": "Ortalar / 90", "Accurate crosses, %": "Başarılı Orta %",
        "Crosses from left flank per 90": "Sol Kanattan Ortalar / 90", "Accurate crosses from left flank, %": "Sol Kanattan Başarılı Ortalar %",
        "Crosses from right flank per 90": "Sağ Kanattan Ortalar / 90", "Accurate crosses from right flank, %": "Sağ Kanattan Başarılı Ortalar %",
        "Crosses to goalie box per 90": "Kaleci Kutusuna Ortalar / 90", "Dribbles per 90": "Dribblingler / 90", "Successful dribbles, %": "Başarılı Dribbling %",
        "Offensive duels per 90": "Hücum İkili Mücadeleleri / 90", "Offensive duels won, %": "Kazanılan Hücum İkili Mücadeleleri %", "Touches in box per 90": "Ceza Sahasında Dokunuşlar / 90",
        "Progressive runs per 90": "Kademeli Taşımalar / 90", "Accelerations per 90": "Topla Hizlanmalar / 90", "Received passes per 90": "Alınan Paslar / 90",   "Received long passes per 90": "Alınan Uzun Paslar / 90",
        "Fouls suffered per 90": "Kazanılan Fauller / 90", "Passes per 90": "Paslar / 90", "Accurate passes, %": "Başarılı Pas %", "Forward passes per 90": "İleri Paslar / 90",
        "Accurate forward passes, %": "Başarılı İleri Paslar %", "Back passes per 90": "Geri Paslar / 90", "Accurate back passes, %": "Başarılı Geri Paslar %",
        "Short / medium passes per 90": "Kısa / Orta Paslar / 90", "Accurate short / medium passes, %": "Başarılı Kısa / Orta Paslar %",
        "Long passes per 90": "Uzun Paslar / 90", "Accurate long passes, %": "Başarılı Uzun Paslar %", "Average pass length, m": "Ortalama Pas Uzunluğu, m",
        "Average long pass length, m": "Ortalama Uzun Pas Uzunluğu, m", "xA per 90": "Beklenen Asist (xA) / 90", "Shot assists per 90": "Şut Asistleri / 90",
        "Second assists per 90": "İkinci Asist / 90", "Third assists per 90": "Üçüncü Asist / 90", "Smart passes per 90": "Akıllı Paslar / 90",
        "Accurate smart passes, %": "Başarılı Akıllı Pas %", "Key passes per 90": "Anahtar Paslar / 90", "Passes to final third per 90": "Son Üçüncüye Paslar / 90",
        "Accurate passes to final third, %": "Son Üçüncüye Başarılı Paslar %", "Passes to penalty area per 90": "Ceza Sahasına Paslar / 90",
        "Accurate passes to penalty area, %": "Ceza Sahasına Başarılı Paslar %", "Through passes per 90": "Ara Paslar / 90",
        "Accurate through passes, %": "Başarılı Ara Paslar %", "Deep completions per 90": "Derin Tamamlamalar / 90",
        "Deep completed crosses per 90": "Derin Tamamlanan Ortalar / 90", "Progressive passes per 90": "Kademeli Paslar / 90",
        "Accurate progressive passes, %": "Başarılı Kademeli Paslar %", "Accurate vertical passes, %": "Başarılı Dikey Paslar %",
        "Vertical passes per 90": "Dikey Paslar / 90", "Conceded goals": "Yenilen Goller", "Conceded goals per 90": "Yenilen Goller / 90",
        "Shots against": "Karşı Şutlar", "Shots against per 90": "Karşı Şutlar / 90", "Clean sheets": "Gol Yememe", "Save rate, %": "Kurtarış Oranı %",
        "xG against": "Karşı Beklenen Gol (xG)", "xG against per 90": "Karşı Beklenen Gol (xG) / 90", "Prevented goals": "Engellenen Goller",
        "Prevented goals per 90": "Engellenen Goller / 90", "Back passes received as GK per 90": "Kaleciye Geri Paslar / 90", "Exits per 90": "Çıkışlar / 90",
        "Aerial duels per 90.1": "Hava Mücadeleleri / 90.1", "Free kicks per 90": "Serbest Vuruşlar / 90", "Direct free kicks per 90": "Direkt Serbest Vuruşlar / 90",
        "Direct free kicks on target, %": "Direkt Serbest Vuruşlar Hedef %", "Corners per 90": "Kornerler / 90", "Penalties taken": "Kullanılan Penaltılar",
        "Penalty conversion, %": "Penaltı Dönüşümü %", "pAdj Tkl+Int per 90": "Top Çalma & Kesmeler (pAdj) / 90", "1st, 2nd, 3rd assists": "1., 2., 3. Asistler",
        "xA per Shot Assist": "xA başına Şut Asisti", "Aerial duels won per 90": "Kazanılan Hava Mücadeleleri / 90", "Cards per 90": "Kartlar / 90",
        "Clean sheets, %": "Gol Yememe %", "npxG": "npxG", "npxG per 90": "npxG / 90", "npxG per shot": "Şut Başına npxG", "Vertical Pass %": "Dikey Pas %"
    }
    return column_mapping

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

def att_winger_schema():
    attacking_winger_schema = {
        'Crossing': {
            'weight': 0.05,
            'measurements': {
                'Ortalar / 90': 0.60,
                'Başarılı Orta %': 0.40
            }
        },
        'Dribbles': {
            'weight': 0.20,
            'measurements': {
                'Dribblingler / 90': 0.65,
                'Başarılı Dribbling %': 0.35
            }
        },
        'Ball Progression': {
            'weight': 0.15,
            'measurements': {
                'Kademeli Taşımalar / 90': 0.35,
                'Topla Hizlanmalar / 90': 0.20,
                'Gol/ Şut %': 0.30,
                'Başarılı Kademeli Paslar %': 0.15
            }
        },
        'Shooting': {
            'weight': 0.25,
            'measurements': {
                'Şutlar / 90': 0.25,
                'Hedefi Bulan Şutlar %': 0.40,
                'Gol/ Şut %': 0.35
            }
        },
        'Defending': {
            'weight': 0.10,
            'measurements': {
                'Top Çalma & Kesmeler (pAdj) / 90': 0.25,
                'Kazanılan Savunma İkili Mücadeleleri %': 0.45,
                'Kazanılan Savunma İkili Mücadeleleri %': 0.30
            }
        },
        'Passing': {
            'weight': 0.10,
            'measurements': {
                'Başarılı Uzun Paslar %': 0.25,
                'Başarılı Uzun Paslar %': 0.05,
                'Başarılı Akıllı Pas %': 0.10,
                'Anahtar Paslar / 90': 0.25,
                'Beklenen Asist (xA) / 90': 0.15,
                'Derin Tamamlamalar / 90': 0.20
            }
        },
        'Penalty Area Entries': {
            'weight': 0.15,
            'measurements': {
                'Ceza Sahasına Paslar / 90': 0.40,
                'Ceza Sahasına Başarılı Paslar %': 0.25,
                'Touches in box per 90': 0.35
            }
        }
    }
    return attacking_winger_schema

position_options = [
    "Forvetler (OOS, K, SF)", "Forvetler ve Kanatlar", "Santrforsuz Forvetler (OOS, K)", 
    "Kanatlar", "Orta Saha (DOS, OS, OOS)", "DOS Olmayan Orta Saha (OS, OOS)",
    "OOS Olmayan Orta Saha (DOS, OS)", "Bekler (FB/KB)", 
    "Defansif Oyuncular (STP, FB/KB, DOS)", "Stoper & Defansif Orta Saha", "Santrforlar", "Stoperler"
]