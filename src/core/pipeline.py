import os
import pandas as pd
import time
from src.core.matching import ProductMatcher

def run_pipeline(input_csv, dataset_csv, output_csv):
    matcher = ProductMatcher(
        index_path="data/processed/product_index.parquet",
        embedding_path="data/processed/product_embeddings.npy",
        model_name='all-MiniLM-L6-v2',
        top_k=10,
        alpha=0.6
    )
    print("📄 Reading input product list...")
    input_df = pd.read_csv(input_csv)
    results = []
    print("🔍 Matching products...")
    start = time.time()
    for prod in input_df['product_name']:
        results.append(matcher.match(prod))
    duration = time.time() - start
    avg_ms = duration / len(input_df) * 1000
    print(f"⏱️ Processed {len(input_df)} items in {duration:.2f}s → {avg_ms:.1f} ms/item")
    # Write results
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f"✅ Matching complete. Results written to: {output_csv}")
