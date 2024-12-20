import numpy as np
import pickle
import faiss 
from sklearn.metrics.pairwise import cosine_similarity

from tqdm import tqdm

def content_based_recommendations(news_embeddings_path, user_profiles, top_k):
    """
    Generate content-based recommendations for each user with similarity scores.

    Args:
        news_embeddings_path (str): Path to the pickle file containing news embeddings.
        user_profiles_path (str): Path to the pickle file containing user profiles.
        top_k (int): Number of recommendations to generate for each user.

    Returns:
        recommendations (dict): Dictionary mapping user_id -> [(news_id, score), ...].
    """
    # Load news embeddings and user profiles
    with open(news_embeddings_path, "rb") as f:
        embedding_data = pickle.load(f)
    news_ids = embedding_data["news_ids"]
    news_embeddings = np.array(embedding_data["embeddings"], dtype=np.float32)


    # Initialize FAISS index for efficient similarity search
    index = faiss.IndexFlatL2(news_embeddings.shape[1])
    index.add(news_embeddings)

    # Recommendations dictionary
    recommendations = {}

    for user_id, user_embedding in tqdm(user_profiles.items(), desc="Content-Based Filtering"):
        # Reshape the user's embedding for FAISS search
        user_embedding = np.array(user_embedding, dtype=np.float32).reshape(1, -1)
        
        # Perform similarity search using FAISS
        distances, similar_indices = index.search(user_embedding, top_k)

        # Convert distances to similarity scores (1 / (1 + distance))
        similarity_scores = 1 / (1 + distances[0])

        # Store news IDs and their scores as a list of tuples
        recommendations[user_id] = [(news_ids[idx], score) for idx, score in zip(similar_indices[0], similarity_scores)]

    return recommendations


#------------------------------------------------------------------------------------

# def content_based_ranking(news_embeddings_path, candidates, user_profiles):
#     """
#     Rank news candidates for each user using content-based similarity.

#     Args:
#         news_embeddings_path (str): Path to the pickled news embeddings file.
#         candidates (dict): Collaborative filtering recommendations {user_id: [news_IDs]}.
#         user_profiles (dict): Dictionary of user profiles {user_id: user_embedding}.

#     Returns:
#         dict: Ranked content-based recommendations {user_id: [news_IDs]}.
#     """
#     # Load news embeddings
#     with open(news_embeddings_path, "rb") as f:
#         embedding_data = pickle.load(f)
#     news_ids = embedding_data["news_ids"]
#     news_embeddings = np.array(embedding_data["embeddings"], dtype=np.float32)

#     # Map news IDs to embeddings
#     news_id_to_embedding = {news_ids[i]: news_embeddings[i] for i in range(len(news_ids))}

#     # Rank news based on content similarity
#     recommendations = {}
#     for user_id, news_candidates in tqdm(candidates.items(), desc="Content-Based Filtering"):
#         user_embedding = np.array(user_profiles[user_id], dtype=np.float32).reshape(1, -1)

#         # Compute similarity for each candidate
#         candidate_scores = {news_id: cosine_similarity(user_embedding, 
#                                                         news_id_to_embedding[news_id].reshape(1, -1))[0, 0]
#                             for news_id in news_candidates if news_id in news_id_to_embedding}

#         # Sort candidates by similarity score
#         ranked_candidates = sorted(candidate_scores, key=candidate_scores.get, reverse=True)
#         recommendations[user_id] = ranked_candidates

#     return recommendations


#-----------------------------------------------------------------------------------------------


# def content_based_recommendation(news_embeddings_path, user_profiles, top_k=10):
#     with open(news_embeddings_path, "rb") as f:
#         embedding_data = pickle.load(f)
#     news_ids = embedding_data["news_ids"]
#     news_embeddings = np.array(embedding_data["embeddings"], dtype=np.float32)
#     index = faiss.IndexFlatL2(news_embeddings.shape[1])
#     index.add(news_embeddings)
#     recommendations = {}
#     for user_id, user_embedding in tqdm(user_profiles.items(), desc="Content-Based Filtering"):
#         user_embedding = np.array(user_embedding, dtype=np.float32).reshape(1, -1)
#         _, similar_indices = index.search(user_embedding, top_k)
#         recommendations[user_id] = [news_ids[idx] for idx in similar_indices[0]]
#     return recommendations
