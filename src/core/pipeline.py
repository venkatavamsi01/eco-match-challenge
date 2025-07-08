import os
import pandas as pd
from src.core.matching import ProductMatcher

def run_pipeline(input_csv, dataset_csv, output_csv):
    matcher = ProductMatcher(
        index_path="data/processed/product_index.parquet",
        embedding_path="data/processed/product_embeddings.npy"
    )

    print("📄 Reading input product list...")
    input_df = pd.read_csv(input_csv)
    results = []

    print("🔍 Matching products...")
    for product in input_df["product_name"]:
        result = matcher.match(product)
        results.append(result)

    print("💾 Saving output...")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f"✅ Matching complete. Results written to: {output_csv}")
