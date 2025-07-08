import pandas as pd
import numpy as np

def load_ingredients(path):
    return pd.read_csv(path)

def save_product_index(df, path):
    df.to_parquet(path, index=False)

def save_embeddings(embeddings, path):
    np.save(path, embeddings)
