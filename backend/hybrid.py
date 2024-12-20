import select
import numpy as np
import pickle
# from tqdm import tqdm
# import faiss
from content_based import content_based_recommendations
from collaborative import collaborative_recommendations
from diversity_ReRank import diversity_re_rank
import numpy as np
import pickle
from tqdm import tqdm

def create_user_profiles(filtered_behaviour_data, news_embeddings_path):
    """
    Create user profiles by averaging news embeddings from users' history.

    Args:
        filtered_behaviour_data (pd.DataFrame): DataFrame containing 'user_id' and 'news_history'.
        news_embeddings_path (str): Path to the pickled file containing news embeddings.

    Returns:
        dict: Dictionary mapping user_id -> user_embedding (np.array).
    """
    # Step 1: Load news embeddings
    with open(news_embeddings_path, "rb") as f:
        embedding_data = pickle.load(f)
    news_id_to_embedding = dict(zip(embedding_data["news_ids"], embedding_data["embeddings"]))

    # Step 2: Initialize user profiles
    user_profiles = {}

    # Step 3: Iterate over users
    for _, row in tqdm(filtered_behaviour_data.iterrows(), total=filtered_behaviour_data.shape[0], desc="Creating User Profiles"):
        user_id = row["user_id"]
        news_history = row["Train_History"]

        # Ensure news_history is a list
        if isinstance(news_history, str):
            news_history = eval(news_history)  # Convert string to list if necessary

        # Retrieve embeddings for the news articles in the user's history
        history_embeddings = np.array([
            news_id_to_embedding[nid]
            for nid in news_history
            if nid in news_id_to_embedding
        ])

        # Step 4: Compute the user's profile embedding
        if len(history_embeddings) > 0:
            user_profiles[user_id] = np.mean(history_embeddings, axis=0)
        else:
            user_profiles[user_id] = np.zeros(embedding_data["embeddings"][0].shape)  # Zero vector

    return user_profiles

def hybrid_recommendations(behavior_data,filtered_data, user_profiles, news_embeddings_path,  similar_users_path, top_k, alpha=0.5):
    """
    Combine CF and CB recommendations into a hybrid with weighted scores.
    
    Args:
        cf_recs (dict): CF recommendations {user_id: [(news_id, score), ...]}.
        cb_recs (dict): CB recommendations {user_id: [(news_id, score), ...]}.
        alpha (float): Weight for CF scores (1 - alpha for CB scores).
    
    Returns:
        dict: Hybrid recommendations {user_id: [(news_id, hybrid_score), ...]}.
    """
    news_embeddings = pickle.load(open(news_embeddings_path, 'rb'))
    similar_users = pickle.load(open(similar_users_path, 'rb'))
    selected_user = {user_id: similar_users[user_id] for user_id in filtered_data['user_id'] if user_id in similar_users}
    selected_user_profile = {user_id: user_profiles[user_id] for user_id in filtered_data['user_id']}
    cf_recs = collaborative_recommendations(
    selected_user, behavior_data, news_embeddings_path, user_profiles, 20)

    cb_recs = content_based_recommendations(news_embeddings_path, selected_user_profile, top_k*2)
    hybrid_recs = {}
    for user_id in cf_recs.keys():
        # Merge scores from CF and CB
        combined_scores = {}
        for news_id, score in cf_recs.get(user_id, []):
            combined_scores[news_id] = alpha * score
        for news_id, score in cb_recs.get(user_id, []):
            combined_scores[news_id] = combined_scores.get(news_id, 0) + (1 - alpha) * score
        
        # Sort by hybrid scores
        sorted_recs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        hybrid_recs[user_id] = sorted_recs[:top_k]  # Limit to top 30
    hybrid_recs = diversity_re_rank(hybrid_recs, news_embeddings, top_k, lambda_div=1)
    # transformed_recommendations = {}

    # for user_id, recommendations in cf_recs.items():
    #     # Extracting news IDs
    #     news_ids = [news_id for news_id, score in recommendations]
    #     transformed_recommendations[user_id] = news_ids
    # return transformed_recommendations
    return hybrid_recs


#--------------------------------------------------------------------------------------

# def hybrid_cf_to_cb(filtered_behaviour_data,filtered_data, user_profiles, news_embeddings_path, similar_users_path, top_n=10):
#     """
#     Generate hybrid recommendations using CF -> CB approach.

#     Args:
#         filtered_behaviour_data (pd.DataFrame): DataFrame containing user_id and news_history.
#         user_profiles (dict): Dictionary of user profiles {user_id: user_embedding}.
#         news_embeddings_path (str): Path to the pickled news embeddings file.
#         top_n (int): Number of final recommendations for each user.

#     Returns:
#         dict: Hybrid recommendations {user_id: [news_IDs]}.
#     """
    
#     # Step 0: Compute similar users
#     similar_users = pickle.load(open(similar_users_path, 'rb'))
#     selected_user = {user_id: similar_users[user_id] for user_id in filtered_data['user_id'] if user_id in similar_users}
    
#     # Step 1: Collaborative filtering to generate candidates
#     cf_candidates = collaborative_recommendations(selected_user, filtered_behaviour_data, top_n * 3)
    
#     # Step 2: Content-based ranking
#     cb_ranked = content_based_ranking(news_embeddings_path, cf_candidates, user_profiles)
    
#     # Step 3: Select top-n recommendations
#     final_recommendations = {user_id: news_list[:top_n] for user_id, news_list in cb_ranked.items()}
    
#     return final_recommendations


# def hybrid_news_recommendation(
#     news_embeddings_path, 
#     filtered_behaviour_data, 
#     alpha=0.5, 
#     top_k=10
# ):
#     """
#     Hybrid recommendation combining content-based and collaborative filtering.

#     Args:
#         news_embeddings_path (str): Path to the pickled news embeddings file.
#         filtered_behaviour_data (pd.DataFrame): DataFrame containing user_id and news_history.
#         alpha (float): Weight for content-based recommendations (0 <= alpha <= 1).
#         top_k (int): Number of recommendations for each user.

#     Returns:
#         dict: Hybrid recommendations {user_id: [news_IDs]}.
#     """
#     # Step 1: Compute user profiles
#     user_profiles = create_user_profiles(filtered_behaviour_data, news_embeddings_path)

#     # Step 2: Generate content-based recommendations
#     content_recs = content_based_recommendation(news_embeddings_path, user_profiles, top_k)

#     # Step 3: Generate collaborative filtering recommendations
#     collaborative_recs = collaborative_filtering_recommendation(filtered_behaviour_data, user_profiles, top_k)

#     # Step 4: Combine recommendations
#     hybrid_recommendations = {}
#     for user_id in user_profiles.keys():
#         # Normalize content and collaborative scores
#         content_scores = {nid: alpha * (1 / (i + 1)) for i, nid in enumerate(content_recs.get(user_id, []))}
#         collaborative_scores = {nid: (1 - alpha) * (1 / (i + 1)) for i, nid in enumerate(collaborative_recs.get(user_id, []))}
        
#         # Merge scores
#         combined_scores = {}
#         for nid in set(content_scores.keys()).union(collaborative_scores.keys()):
#             combined_scores[nid] = content_scores.get(nid, 0) + collaborative_scores.get(nid, 0)

#         # Sort and pick top-k recommendations
#         sorted_recs = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
#         hybrid_recommendations[user_id] = [nid for nid, _ in sorted_recs[:top_k]]

#     return hybrid_recommendations

