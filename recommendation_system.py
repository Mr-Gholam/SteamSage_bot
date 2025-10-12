import os
import pandas as pd
import numpy as np
from langdetect import detect, DetectorFactory
from scipy.sparse import csr_matrix, hstack
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import pickle

# ----------- 1. Data Loading -----------
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path, low_memory=False)
    print(f"File '{path}' not found.")
    return None

recommendation = load_csv("./Dataset/recommendations.csv")
games = load_csv("./Dataset/games.csv")
users = load_csv("./Dataset/users.csv")
steam_games = load_csv("./Dataset/steam_games.csv")

# ----------- 2. Data Cleaning (Optional) -----------
if steam_games is not None:
    steam_games_clean = steam_games[["AppID", "Name", "Categories", "Genres"]]

# ----------- 3. Collaborative Filtering -----------
def collaborative_setup(games, recommendation):
    merged = games.merge(recommendation, on='app_id')
    user_count = merged['user_id'].value_counts()
    game_count = merged['title'].value_counts()
    filtered = merged[
        merged['user_id'].isin(user_count[user_count >= 400].index) &
        merged['title'].isin(game_count[game_count >= 250].index)
    ]
    pt = filtered.pivot_table(index='title', columns='user_id', values='is_recommended', fill_value=0)
    svd = TruncatedSVD(n_components=50)
    reduced = svd.fit_transform(pt)
    reduced = normalize(reduced)
    sim_matrix = cosine_similarity(reduced)
    return pt, sim_matrix

def recommend_based_on_collaborative(game, pt, sim_matrix):
    if game not in pt.index:
        return []
    idx = list(pt.index).index(game)
    sim_games = sorted(list(enumerate(sim_matrix[idx])), key=lambda x: x[1], reverse=True)[1:6]
    return [pt.index[i[0]] for i in sim_games]

# ----------- 4. Content Based Filtering -----------
def content_setup(games):
    warnings.filterwarnings("ignore", category=UserWarning)
    DetectorFactory.seed = 0

    def get_language(text):
        try:
            return detect(text)
        except Exception:
            return None

    games['detected_language'] = games['title'].apply(get_language)
    games_en = games[games['detected_language'] == 'en'].copy()
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vector = cv.fit_transform(games_en['title'])

    # Numeric features
    games_en['date_release'] = pd.to_datetime(games_en['date_release'])
    games_en['release_year'] = games_en['date_release'].dt.year
    scaler = MinMaxScaler()
    games_en['release_year'] = scaler.fit_transform(games_en[['release_year']])
    games_en['positive_ratio'] = scaler.fit_transform(games_en[['positive_ratio']])
    games_en['price_final'] = scaler.fit_transform(games_en[['price_final']])
    scaled_features = csr_matrix(games_en[['positive_ratio', 'price_final', 'release_year']])

    ratings_categories = [
        'Overwhelmingly Negative', 'Very Negative', 'Mostly Negative', 'Negative',
        'Mixed', 'Positive', 'Mostly Positive', 'Very Positive', 'Overwhelmingly Positive'
    ]
    oe = OrdinalEncoder(categories=[ratings_categories])
    games_en.loc[:, 'rating'] = oe.fit_transform(games_en[['rating']])
    ratings_encoded = games_en['rating'].values.reshape(-1, 1)

    # Binary features
    games_en['win'] = games_en['win'].astype(int)
    games_en['mac'] = games_en['mac'].astype(int)
    games_en['linux'] = games_en['linux'].astype(int)
    binary_features = csr_matrix(games_en[['win', 'mac', 'linux']])

    combined = hstack([
        vector,
        csr_matrix(ratings_encoded.astype(float)),
        scaled_features,
        binary_features
    ])

    combined = csr_matrix(combined)
    sim_matrix = cosine_similarity(combined)
    games_en = games_en.drop(
        columns=['date_release', 'user_reviews', 'price_original', 'discount', 'steam_deck', 'detected_language'],
        errors='ignore'
    )
    final_df = games_en.set_index('app_id', drop=True)
    sim_df = pd.DataFrame(sim_matrix, index=final_df.index, columns=final_df.index)
    title_df = games_en[['app_id', 'title']].set_index('app_id', drop=True)
    return title_df, sim_df

def recommend_based_on_content(title, title_df, sim_df):
    matching_games = title_df[title_df['title'] == title]
    if len(matching_games) == 0:
        return []
    game_id = matching_games.index[0]
    sorted_scores = sim_df.loc[game_id].sort_values(ascending=False)
    recommendations = sorted_scores[sorted_scores.index != game_id].head(5)
    return [title_df.loc[i]['title'] for i in recommendations.index]

# ----------- 5. Build Models and Save to PKL -----------
if recommendation is not None and games is not None:
    pt, collab_sim_matrix = collaborative_setup(games, recommendation)
    title_df, content_sim_df = content_setup(games)

    # Save collaborative filtering objects
    with open('collaborative_recommender.pkl', 'wb') as f:
        pickle.dump({'pt': pt, 'collab_sim_matrix': collab_sim_matrix}, f)

    # Save content-based filtering objects
    with open('content_recommender.pkl', 'wb') as f:
        pickle.dump({'title_df': title_df, 'content_sim_df': content_sim_df}, f)

    print("Saved collaborative_recommender.pkl and content_recommender.pkl!")

    # Example usage (comment out for production)
    print("Collaborative:", recommend_based_on_collaborative("Just Cause™ 3", pt, collab_sim_matrix))
    print("Content-based:", recommend_based_on_content('BRINK: Agents of Change', title_df, content_sim_df))
    print("DONE")