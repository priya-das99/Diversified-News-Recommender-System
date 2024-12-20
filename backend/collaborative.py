import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
import ast
# similar_users_path='data/processed_data/similar_users_faiss.pkl'



import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from collections import Counter

def collaborative_recommendations(similar_users, behavior_data, news_embeddings_path, user_profiles, top_k=30):
    """
    Generate recommendations for each user based on similar users' history,
    with scores based on cosine similarity with the user's profile.

    Args:
        similar_users (dict): User similarity dictionary (user_id -> [(similar_user_id, similarity_score), ...]).
        behavior_data (pd.DataFrame): DataFrame containing 'user_id', 'Train_History', and 'Test_History'.
        news_embeddings_path (str): Path to the pickle file containing news embeddings.
        user_profiles_path (str): Path to the pickle file containing user profiles.
        top_k (int): Number of recommendations to generate for each user.

    Returns:
        recommendations (dict): Dictionary mapping user_id -> [(news_id, score), ...].
    """
    # Load news embeddings and user profiles
    with open(news_embeddings_path, "rb") as f:
        news_embeddings_data = pickle.load(f)
    news_embeddings = dict(zip(news_embeddings_data["news_ids"], news_embeddings_data["embeddings"]))

    # with open(user_profiles_path, "rb") as f:
    #     user_profiles = pickle.load(f)

    # Convert behavior_data to a dictionary for faster access
    user_train_history = behavior_data.set_index('user_id')['Train_History'].to_dict()

    recommendations = {}

    for user_id, similar_user_list in tqdm(similar_users.items(), desc="Collaborative Filtering"):
        # Get the current user's train history and profile
        current_user_seen = user_train_history.get(user_id, [])
        user_profile = user_profiles.get(user_id, None)

        if user_profile is None:
            continue  # Skip if no profile exists for the user

        # Gather all news IDs from similar users' train history
        similar_users_news = []
        for similar_user_id, _ in similar_user_list:
            similar_users_news += ast.literal_eval(user_train_history.get(similar_user_id, []))

        # Filter unseen news for the current user
        unseen_news = [news_id for news_id in similar_users_news if news_id not in current_user_seen]

        # Count frequencies of unseen news
        news_frequency = Counter(unseen_news)

        # Calculate cosine similarity scores for the unseen news
        scores = []
        for news_id, freq in news_frequency.items():
            if news_id in news_embeddings:
                news_embedding = np.array(news_embeddings[news_id]).reshape(1, -1)
                user_profile = np.array(user_profile).reshape(1, -1)
                similarity = cosine_similarity(user_profile, news_embedding)[0, 0]
                scores.append((news_id, similarity))

        # Sort by similarity score (descending) and take the top_k news IDs
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

        # Save recommendations for the user
        recommendations[user_id] = sorted_scores

    return recommendations


# def collaborative_recommendations(similar_users, behavior_data, top_k=10):
#     """
#     Generate recommendations for each user based on similar users' history.

#     Args:
#         similar_users (dict): User similarity dictionary (user_id -> [(similar_user_id, similarity_score), ...]).
#         behavior_data (pd.DataFrame): DataFrame containing 'User ID', 'Train_History', and 'Test_History'.
#         top_k (int): Number of recommendations to generate for each user.

#     Returns:
#         recommendations (dict): Dictionary mapping user_id -> [recommended_news_ids].
#     """
#     # Initialize recommendations dictionary
#     recommendations = {}
 
#     # Convert behavior_data to a dictionary for faster access
#     user_train_history = behavior_data.set_index('user_id')['Train_History'].to_dict()

#     for user_id, similar_user_list in tqdm(similar_users.items(),desc="Collaborative Filtering"):
#         # Get the current user's train history
#         current_user_seen = user_train_history.get(user_id, [])
       
       
        
#         # Gather all news IDs from similar users' train history
#         similar_users_news = []
#         for similar_user_id, _ in similar_user_list:  # Ignore similarity score
            
#             similar_users_news += ast.literal_eval(user_train_history.get(similar_user_id, []))
           
#         # Filter unseen news for the current user
#         unseen_news = [news_id for news_id in similar_users_news if news_id not in current_user_seen]

#         # Count frequencies of unseen news
#         from collections import Counter
#         news_frequency = Counter(unseen_news)

#         # Sort by frequency (descending) and take the top_k news IDs
#         sorted_news = [news_id for news_id, _ in news_frequency.most_common(top_k)]

#         # Add to recommendations
#         recommendations[user_id] = sorted_news

#     return recommendations
