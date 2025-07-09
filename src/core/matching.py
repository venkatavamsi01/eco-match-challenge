import numpy as np
import pandas as pd
from thefuzz import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from src.core.cleaning import clean_text

class ProductMatcher:
    def __init__(
        self,
        index_path: str,
        embedding_path: str,
        model_name: str = 'all-MiniLM-L6-v2',
        top_k: int = 10,
        alpha: float = 0.5
    ):
        # Load your precomputed index and embeddings
        self.index_df = pd.read_parquet(index_path)
        self.embeddings = np.load(embedding_path)
        self.embedder = SentenceTransformer(model_name)
        self.top_k = top_k
        self.alpha = alpha

    def match(self, raw_name: str) -> dict:
        # 1) Clean input
        cleaned = clean_text(raw_name)

        # 2) Embed
        query_vec = self.embedder.encode([cleaned])[0]

        # 3) Compute cosine similarities
        sims = cosine_similarity([query_vec], self.embeddings)[0]

        # 4) Retrieve top-K candidates by embedding score
        top_idx = np.argsort(sims)[-self.top_k:][::-1]

        # 5) Re-rank with fuzzy string score
        best_idx, best_score = top_idx[0], -np.inf
        for idx in top_idx:
            # Use the 'cleaned' column from the index
            candidate_clean = self.index_df.iloc[idx]['cleaned']
            fuzzy_score = fuzz.token_sort_ratio(cleaned, candidate_clean) / 100.0
            combined = self.alpha * sims[idx] + (1 - self.alpha) * fuzzy_score
            if combined > best_score:
                best_idx, best_score = idx, combined

        chosen = self.index_df.iloc[best_idx]
        return {
            'input_product': raw_name,
            'matched_product': chosen['name'],
            'carbon_rating': chosen['carbon_rating']
        }
