import pickle
import random

# ---- Load Collaborative Filtering objects ----
with open('Pkl/collaborative_recommender.pkl', 'rb') as f:
    collab = pickle.load(f)
pt = collab['pt']
collab_sim_matrix = collab['collab_sim_matrix']

def recommend_based_on_collaborative(game, pt, sim_matrix):
    """
    Try to find recommendations using collaborative filtering.
    Performs case-insensitive partial matching if exact match fails.
    """
    # Try direct (case-sensitive) match
    if game in pt.index:
        idx = list(pt.index).index(game)
    else:
        # Case-insensitive partial match
        matches = [i for i, t in enumerate(pt.index) if game.lower() in t.lower()]
        if not matches:
            print(f"No match for '{game}'. Available examples: {list(pt.index[:10])}")
            return []
        idx = matches[0]
    sim_games = sorted(list(enumerate(sim_matrix[idx])), key=lambda x: x[1], reverse=True)[1:6]
    return [pt.index[i[0]] for i in sim_games]

def collaborative(name):
    """
    Interface for collaborative recommendations.
    """
    return recommend_based_on_collaborative(name, pt, collab_sim_matrix)

# ---- Load Content-Based Filtering objects ----
with open('Pkl/content_recommender.pkl', 'rb') as f:
    content = pickle.load(f)
title_df = content['title_df']
content_sim_df = content['content_sim_df']

def recommend_based_on_content(title, title_df, sim_df):
    """
    Find recommendations using content-based filtering.
    Falls back to case-insensitive partial match if exact title is not found.
    """
    matching_games = title_df[title_df['title'] == title]
    if len(matching_games) == 0:
        # Try case-insensitive partial match
        matches = title_df[title_df['title'].str.lower().str.contains(title.lower())]
        if matches.empty:
            print(f"Game '{title}' not found in the dataset.")
            print("Available games (first 10):")
            print(title_df['title'].head(10).tolist())
            return []
        game_id = matches.index[0]
    else:
        game_id = matching_games.index[0]
    sorted_scores = sim_df.loc[game_id].sort_values(ascending=False)
    recommendations = sorted_scores[sorted_scores.index != game_id].head(5)
    return [title_df.loc[i]['title'] for i in recommendations.index]

def content_based(name):
    """
    Interface for content-based recommendations.
    """
    return recommend_based_on_content(name, title_df, content_sim_df)

# ---- Hybrid Recommender ----
def hybrid(name):
    """
    Tries collaborative first, then content-based, then merges unique results.
    """
    recs_collab = collaborative(name)
    recs_content = content_based(name)
    # Merge, keeping order: collaborative first, then unique from content
    seen = set(recs_collab)
    merged = recs_collab + [g for g in recs_content if g not in seen]
    random.shuffle(merged)
    return merged[:5]

# ---- Example Usage ----
# Uncomment to test in your environment

# game_name = "dota"
# print("Collaborative Recommendations for:", game_name)
# print(collaborative(game_name))

# title = "dota"
# print("Content-Based Recommendations for:", title)
# print(content_based(title))

# print("Hybrid Recommendations for:", game_name)
# print(hybrid(game_name))