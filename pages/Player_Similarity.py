import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from scripts import utils
from scripts.config import get_position_to_schema, get_params_list, get_schema_params, get_label_mapping, get_column_mapping, position_options

st.set_page_config(page_title="Player Similarity Finder")

@st.cache_data
def load_data(df):
    
    df = df[['Player', 'Age', 'Main Position', 'Minutes played', 'Goals', 'xG', 'Assists', 'xA', 'Duels per 90', 'Duels won, %']]
    # df = df[['Oyuncu', 'Yaş', 'Ana Pozisyon', 'Oynadığı dakikalar', 'Goller', 'Beklenen Gol (xG)', 'Asistler', 'Beklenen Asist (xA)', 'İkili Mücadeleler / 90', 'Kazanılan İkili Mücadeleler %']]
    # Replace NaN values with 0
    df.fillna(0, inplace=True)

    # Remove '%' symbol from percentage columns and convert to numeric values
    percentage_cols = [col for col in df.columns if df[col].astype(str).str.contains('%').any()]
    for col in percentage_cols:
        df[col] = df[col].str.replace('%', '').astype(float)

    # Replace infinity values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Fill NaN values with 0 (or use another appropriate fill method)
    df.fillna(0, inplace=True)

    # Select the numerical columns for generating vector embeddings
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    numerical_cols = [col for col in numerical_cols if col != 'Unnamed: 0']

    # Standardize the numerical columns
    scaler = StandardScaler()
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    # Generate vector embeddings (as numpy array)
    vector_embeddings = df[numerical_cols].values

    # Create a similarity matrix based on cosine similarity
    similarity_matrix = cosine_similarity(vector_embeddings)

    # # Strip leading/trailing spaces from player names
    # df['Name'] = df['Name'].str.strip()

    # Convert the numpy array to a DataFrame for easier handling
    similarity_df = pd.DataFrame(similarity_matrix, index=df['Oyuncu'], columns=df['Oyuncu'])

    return df, similarity_df

def get_similar_players(df, similarity_df, player_name, top_n=10):
    # Get the similarity scores for the given player
    similarity_scores = similarity_df[player_name]

    # Sort the scores in descending order and take the top_n players
    most_similar_players = similarity_scores.sort_values(ascending=False).head(top_n + 1)

    # Exclude the player themselves from the list
    most_similar_players = most_similar_players[most_similar_players.index != player_name]

    # Create a DataFrame with names and positions of the similar players
    similar_players_df = pd.DataFrame(most_similar_players).join(df.set_index('Oyuncu')[['Ana Pozisyon']])

    # Rename the columns
    similar_players_df.columns = ['Similarity', 'Ana Pozisyon']

    return similar_players_df

# Add title
st.title("Player Similarity Finder")

league_list = list(utils.load_lg_data())
selected_leagues = st.sidebar.multiselect("Lig Seçiniz", league_list)
# selected_season = st.sidebar.selectbox("Sezon Seçiniz", utils.load_lg_data(selected_leagues))

# Function to load data for multiple leagues
def load_multiple_leagues(selected_leagues, selected_season):
    combined_data = pd.DataFrame()
    for league in selected_leagues:
        league_data = utils.load_player_data(league, selected_season)
        combined_data = pd.concat([combined_data, league_data], ignore_index=True)
    return combined_data

# Load the data for the selected leagues and season
if selected_leagues:
    league_season_data = load_multiple_leagues(selected_leagues, "23-24")
    
selected_position = st.sidebar.selectbox("Pozisyon Seçiniz", position_options)
min_minutes_played = st.sidebar.number_input("Minimum Oynanan Dakikalar", value=900, min_value=0)
max_age = st.sidebar.slider("Max Yaş", min_value=15, max_value=38, value=30)

filtered_data, top_5_league_data = utils.filter_data(league_season_data, selected_position, min_minutes_played, max_age)

st.write(filtered_data)

# # Load the data
df, similarity_df = load_data(filtered_data)

player_name = st.selectbox("Futbolcu Adı", df['Oyuncu'])
# Select number of similar players to display
top_n = st.slider('Select number of similar players to display', min_value=1, max_value=50, value=10)

# Button to get similar players
if st.button('Get Similar Players'):
    # Get the most similar players
    similar_players = get_similar_players(df, similarity_df, player_name, top_n)

    # Display the similar players
    st.write(similar_players)