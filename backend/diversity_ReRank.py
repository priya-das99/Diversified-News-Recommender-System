def diversity_re_rank(hybrid_recs, news_embeddings, top_k=10, lambda_div=0.5):
    """
    Re-rank hybrid recommendations to improve diversity.
    
    Args:
        hybrid_recs (dict): Hybrid recommendations {user_id: [(news_id, score), ...]}.
        news_embeddings (dict): Embeddings for each news item {news_id: embedding}.
        top_k (int): Number of recommendations to retain after re-ranking.
        lambda_div (float): Weight for diversity in the ranking algorithm.
    
    Returns:
        dict: Re-ranked recommendations {user_id: [news_id, ...]}.
    """
    re_ranked_recs = {}
    for user_id, recommendations in hybrid_recs.items():
        selected_news = []
        candidate_news = [rec[0] for rec in recommendations]
        
        while len(selected_news) < top_k and candidate_news:
            # Compute diversity scores for each candidate
            diversity_scores = []
            for news_id in candidate_news:
                if not selected_news:
                    diversity_scores.append(1)  # First news is always included
                else:
                    # Compute similarity with already selected news
                    similarities = [
                        cosine_similarity([news_embeddings[news_id]], [news_embeddings[selected]])[0][0]
                        for selected in selected_news
                        if selected in news_embeddings
                    ]
                    diversity_score = 1 - max(similarities) if similarities else 1
                    diversity_scores.append(diversity_score)
            
            # Combine diversity and relevance scores
            relevance_scores = [rec[1] for rec in recommendations if rec[0] in candidate_news]
            combined_scores = [
                lambda_div * div + (1 - lambda_div) * rel
                for div, rel in zip(diversity_scores, relevance_scores)
            ]
            
            # Select the news with the highest combined score
            best_idx = combined_scores.index(max(combined_scores))
            selected_news.append(candidate_news.pop(best_idx))
        
        re_ranked_recs[user_id] = selected_news
    return re_ranked_recs
