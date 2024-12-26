import pandas as pd
import pickle
import json
from collections import Counter
from .hybrid import hybrid_recommendations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dummy data for demonstration purposes
users = {
    'U28014': 'pass1',
    'U57061': 'pass2',
    'user3':'pass3',
    'U10034':'pass4'
}

behaviour_data = pd.read_csv('data/behaviour_data.csv')
news_data = pd.read_csv('data/news_data.csv')
news_embeddings_path = 'data/processed_data/news_embeddings.pkl'
user_profiles_path = 'data/processed_data/user_profile.pkl'
news_frequency_path = 'data/processed_data/news_to_frequency.json'
similar_users_path='data/processed_data/similar_users_faiss.pkl'


def authenticate_user(user_id, password):
    return users.get(user_id) == password
def get_trending_news():
    # Load the news frequency data from the JSON file
    with open(news_frequency_path, 'r') as f:
        news_frequency = json.load(f)

    # Get the top 10 news IDs based on frequency
    top_news_ids = [news_id for news_id, _ in sorted(news_frequency.items(), key=lambda item: item[1], reverse=True)[:10]]
    trending_news = news_data[news_data['News_ID'].isin(top_news_ids)].to_dict(orient='records')
    return trending_news

def get_recommended_news(user_id):
    with open(news_embeddings_path, 'rb') as f:
        news_embeddings = pickle.load(f)
    with open(user_profiles_path, 'rb') as f:
        user_profiles = pickle.load(f)

    user_embedding = user_profiles.get(user_id)
    if user_embedding is None:
        return []

    # Use the hybrid recommendation algorithm
    filtered_data = behaviour_data[behaviour_data['user_id'] == user_id]
    
    hybrid_recs =  hybrid_recommendations(behaviour_data, filtered_data,user_profiles, news_embeddings_path,similar_users_path, top_k=10, alpha=0.5)
    recommended_news_ids = hybrid_recs.get(user_id, [])
    recommended_news = news_data[news_data['News_ID'].isin(recommended_news_ids)].to_dict(orient='records')

    return recommended_news

def get_news_by_id(news_id):
    try:
        news_item = news_data[news_data['News_ID'] == news_id]
        if not news_item.empty:
            return news_item.to_dict(orient='records')[0]
        else:
            logger.warning(f"News_ID {news_id} not found.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving news by ID: {e}")
        return None

def track_news_click(user_id, news_id):
    try:
        # Update behaviour_data.csv
        global behaviour_data
        new_interaction = pd.DataFrame({
            'user_id': [user_id],
            'News_ID': [news_id],
            'Train_History': [[news_id]]  # Add as a list since Train_History is a list column
        })
        
        # If user exists, append to their Train_History
        if user_id in behaviour_data['user_id'].values:
            user_idx = behaviour_data[behaviour_data['user_id'] == user_id].index[0]
            current_history = behaviour_data.at[user_idx, 'Train_History']
            if isinstance(current_history, str):
                current_history = eval(current_history)
            if not isinstance(current_history, list):
                current_history = []
            current_history.append(news_id)
            behaviour_data.at[user_idx, 'Train_History'] = current_history
        else:
            behaviour_data = pd.concat([behaviour_data, new_interaction], ignore_index=True)
        
        # Save updated behaviour_data
        behaviour_data.to_csv('data/behaviour_data.csv', index=False)

        # Update news frequency
        with open(news_frequency_path, 'r') as f:
            news_frequency = json.load(f)
        
        news_frequency[news_id] = news_frequency.get(news_id, 0) + 1
        
        with open(news_frequency_path, 'w') as f:
            json.dump(news_frequency, f)

        # Update user profile
        with open(news_embeddings_path, 'rb') as f:
            news_embeddings = pickle.load(f)
        
        with open(user_profiles_path, 'rb') as f:
            user_profiles = pickle.load(f)
        
        # Get the news embedding
        news_embedding = news_embeddings.get(news_id)
        if news_embedding is not None:
            # Update user profile with new embedding
            if user_id in user_profiles:
                # Simple averaging strategy
                current_profile = user_profiles[user_id]
                updated_profile = [(a + b)/2 for a, b in zip(current_profile, news_embedding)]
                user_profiles[user_id] = updated_profile
            else:
                user_profiles[user_id] = news_embedding
            
            # Save updated user profiles
            with open(user_profiles_path, 'wb') as f:
                pickle.dump(user_profiles, f)
        
        return True
    except Exception as e:
        logger.error(f"Error tracking news click: {e}")
        return False
