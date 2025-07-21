import numpy as np
import pandas as pd
import faiss
from thefuzz import fuzz
from sentence_transformers import SentenceTransformer
from core.cleaning import clean_text

class ProductMatcher:
    def __init__(
        self,
        index_path: str,
        embedding_path: str,
        model_name: str = 'all-MiniLM-L6-v2',
        top_k: int = 10,
        alpha: float = 0.5
    ):
        # 1) Load your precomputed index and embeddings
        self.index_df   = pd.read_parquet(index_path)
        self.embeddings = np.load(embedding_path)
        self.embedder   = SentenceTransformer(model_name)
        self.top_k      = top_k
        self.alpha      = alpha

        # build an exact Inner‑Product FAISS index over normalized vectors
        emb_norm = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )
        d = emb_norm.shape[1]
        self.faiss_index = faiss.IndexFlatIP(d)
        self.faiss_index.add(emb_norm)

    def match(self, raw_name: str) -> dict:
        # 1) Clean & embed
        cleaned   = clean_text(raw_name)
        query_vec = self.embedder.encode([cleaned])[0]

        # 2) exact top‑K by cosine (as IP) via FAISS
        q_norm, = (query_vec / np.linalg.norm(query_vec)).reshape(1, -1)
        sims, top_idx = self.faiss_index.search(q_norm.reshape(1, -1), self.top_k)
        sims, top_idx = sims[0], top_idx[0]

        # 3) Re‑rank those K with your α·semantic + (1−α)·fuzzy blend
        best_idx, best_score = top_idx[0], -np.inf
        for sim, idx in zip(sims, top_idx):
            candidate_clean = self.index_df.iloc[idx]['cleaned']
            fuzzy_score     = fuzz.token_sort_ratio(cleaned, candidate_clean) / 100.0
            combined        = self.alpha * sim + (1 - self.alpha) * fuzzy_score
            if combined > best_score:
                best_idx, best_score = idx, combined

        chosen = self.index_df.iloc[best_idx]
        return {
            'input_product':   raw_name,
            'matched_product': chosen['name'],
            'carbon_rating':   chosen['carbon_rating']
        }
