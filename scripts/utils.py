# utils.py
import pandas as pd

def filter_by_position(df, position):
    fw = ["CF", "RW", "LW", "AMF"]
    if position == "Forvetler (OOS, K, SF)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(fw), na=False)]
    
    stw = ["CF", "RW", "LW", "LAMF", "RAMF"]
    if position == "Forvetler ve Kanatlar":
        return df[df['Ana Pozisyon'].str.contains('|'.join(stw), na=False)]
    
    fwns = ["RW", "LW", "AMF"]
    if position == "Santrforsuz Forvetler (OOS, K)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(fwns), na=False)]
    
    wing = ["RW", "LW", "WF", "LAMF", "RAMF"]
    if position == "Kanatlar":
        return df[df['Ana Pozisyon'].str.contains('|'.join(wing), na=False)]

    mids = ["DMF", "CMF", "AMF"]
    if position == "Orta Saha (DOS, OS, OOS)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(mids), na=False)]

    cms = ["CMF", "AMF"]
    if position == "DOS Olmayan Orta Saha (OS, OOS)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(cms), na=False)]

    dms = ["CMF", "DMF"]
    if position == "OOS Olmayan Orta Saha (DOS, OS)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(dms), na=False)]

    fbs = ["LB", "RB", "WB"]
    if position == "Bekler (FB/KB)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(fbs), na=False)]

    defs = ["LB", "RB", "WB", "CB", "DMF"]
    if position == "Defansif Oyuncular (STP, FB/KB, DOS)":
        return df[df['Ana Pozisyon'].str.contains('|'.join(defs), na=False)]

    cbdm = ["CB", "DMF"]
    if position == "Stoper & Defansif Orta Saha":
        return df[df['Ana Pozisyon'].str.contains('|'.join(cbdm), na=False)]

    cf = ["CF"]
    if position == "Santrforlar":
        return df[df['Ana Pozisyon'].str.contains('|'.join(cf), na=False)]

    cb = ["CB"]
    if position == "Stoperler":
        return df[df['Ana Pozisyon'].str.contains('|'.join(cb), na=False)]
    else:
        return df

# Function to load data for the Top 5 Leagues
def load_top_5_leagues():
    top_5_leagues = ["La Liga 23-24", "Premier League 23-24", "Bundesliga 23-24", "Serie A 23-24", "Ligue 1 23-24"]
    top_5_league_data = []
    for league in top_5_leagues:
        league_data = read_csv2((f'https://raw.githubusercontent.com/griffisben/Wyscout_Prospect_Research/main/Main%20App/{league.replace(" ","%20").replace("ü","u").replace("ó","o").replace("ö","o")}.csv'))
        league_data = league_data[list(schemas.column_mapping().values())]
        league_data['Lig'] = league
        top_5_league_data.append(league_data)
    return pd.concat(top_5_league_data, ignore_index=True)

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
    df['Ana Pozisyon'] = df['Position'].str.split().str[0].str.rstrip(',')
    df = df.dropna(subset=['Ana Pozisyon']).reset_index(drop=True)
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
    
    df['Ana Pozisyon'] = df['Ana Pozisyon'].replace(position_replacements)
    df.fillna(0,inplace=True)
    df.rename(columns=schemas.column_mapping(), inplace=True)
  
    return df

def rank_column(df, column_name):
    return stats.rankdata(df[column_name], "average") / len(df[column_name])
