import os
import pandas as pd
from core.io import load_ingredients, save_product_index, save_embeddings
from core.cleaning import clean_text
from core.embedding import embed_texts

RAW_DATA_PATH = 'src/data/open-source-ingredients.csv'
PROCESSED_INDEX_PATH = 'data/processed/product_index.parquet'
EMBEDDINGS_PATH = 'data/processed/product_embeddings.npy'

def preprocess():
    print("📥 Loading raw ingredient dataset...")
    df = load_ingredients(RAW_DATA_PATH)

    print("🧼 Cleaning product names...")
    df['cleaned'] = df['clean name'].astype(str).apply(clean_text)

    print("🔢 Generating embeddings...")
    embeddings = embed_texts(df['cleaned'].tolist())

    print("💾 Saving cleaned index and embeddings...")
    os.makedirs('data/processed', exist_ok=True)
    save_product_index(df, PROCESSED_INDEX_PATH)
    save_embeddings(embeddings, EMBEDDINGS_PATH)

    print("✅ Preprocessing complete!")

if __name__ == "__main__":
    preprocess()
