import pickle

# ---- Load Collaborative Filtering objects ----
with open('collaborative_recommender.pkl', 'rb') as f:
    collab = pickle.load(f)
pt = collab['pt']
collab_sim_matrix = collab['collab_sim_matrix']



def recommend_based_on_collaborative(game, pt, sim_matrix):
    # Try direct match
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

# ---- Load Content-Based Filtering objects ----
with open('content_recommender.pkl', 'rb') as f:
    content = pickle.load(f)
title_df = content['title_df']
content_sim_df = content['content_sim_df']

def recommend_based_on_content(title, title_df, sim_df):
    matching_games = title_df[title_df['title'] == title]
    if len(matching_games) == 0:
        print(f"Game '{title}' not found in the dataset.")
        print("Available games (first 10):")
        print(title_df['title'].head(10).tolist())
        return []
    game_id = matching_games.index[0]
    sorted_scores = sim_df.loc[game_id].sort_values(ascending=False)
    recommendations = sorted_scores[sorted_scores.index != game_id].head(5)
    return [title_df.loc[i]['title'] for i in recommendations.index]

# ---- Example Usage ----

# game_name = "dota"
# print("Collaborative Recommendations for:", game_name)
# print(recommend_based_on_collaborative(game_name, pt, collab_sim_matrix))




def collaborative(name):
   return recommend_based_on_collaborative(name, pt, collab_sim_matrix)

# title = "BRINK: Agents of Change"
# print("Content-Based Recommendations for:", title)
# print(recommend_based_on_content(title, title_df, content_sim_df))



# print("Available collaborative titles (first 10):", list(pt.index[:10]))
# print("Available content titles (first 10):", title_df['title'].head(10).tolist())

# print("Looking for:", game_name in pt.index)  # should be True
# print("Looking for:", title in title_df['title'].values)  # should be True

# print([t for t in pt.index if "just cause" in t.lower()])

# print("pt shape:", pt.shape)
# print("title_df shape:", title_df.shape)