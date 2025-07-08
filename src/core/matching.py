import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from src.core.cleaning import clean_text
from src.core.embedding import embed_texts

class ProductMatcher:
    def __init__(self, index_path, embedding_path):
        self.index_df = pd.read_parquet(index_path)
        self.embeddings = np.load(embedding_path)

    def match(self, product_name):
        cleaned = clean_text(product_name)
        query_vector = embed_texts([cleaned])[0].reshape(1, -1)
        similarities = cosine_similarity(query_vector, self.embeddings)[0]
        best_match_idx = np.argmax(similarities)
        best_match = self.index_df.iloc[best_match_idx]

        return {
            "input_product": product_name,
            "matched_product": best_match["name"],
            "carbon_rating": best_match["carbon_rating"]
        }
