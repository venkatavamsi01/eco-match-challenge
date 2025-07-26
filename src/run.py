import time
import pandas as pd
from core.pipeline import run_pipeline
from core.matching import ProductMatcher

def run_timed_pipeline():
    input_csv = "src/data/test.csv"
    output_csv = "output/output.csv"
    index_path = "data/processed/product_index.parquet"
    faiss_path = "data/processed/faiss_index.bin"

    # ⏱️ Step 1: Load matcher (index, embedder, FAISS)
    print("⏳ Loading matcher...")
    t0 = time.time()
    matcher = ProductMatcher(
        index_path=index_path,
        embedding_path=None,
        model_name="all-MiniLM-L6-v2",
        top_k=10,
        alpha=0.6
    )
    t1 = time.time()
    print(f"✅ Matcher loaded in {(t1 - t0)*1000:.2f} ms")

    # ⏱️ Step 2: Load input CSV
    print("📄 Loading input file...")
    t2 = time.time()
    input_df = pd.read_csv(input_csv)
    t3 = time.time()
    print(f"✅ Loaded {len(input_df)} rows in {(t3 - t2)*1000:.2f} ms")

    # ⏱️ Step 3: Match all products
    results = []
    print("🚀 Matching products...")
    total_match_time = 0
    for i, prod in enumerate(input_df["product_name"]):
        t_start = time.time()
        match_result = matcher.match(prod)
        t_end = time.time()
        match_time = (t_end - t_start) * 1000
        total_match_time += match_time
        results.append(match_result)
        print(f"[{i+1}/{len(input_df)}] Matched in {match_time:.2f} ms")

    avg_match_time = total_match_time / len(input_df)

    # ⏱️ Step 4: Write output
    print("💾 Writing output file...")
    t4 = time.time()
    pd.DataFrame(results).to_csv(output_csv, index=False)
    t5 = time.time()
    print(f"✅ Output written in {(t5 - t4)*1000:.2f} ms")

    # 📊 Summary
    total_runtime = t5 - t0
    print("\n📊 Benchmark Summary")
    print("----------------------------")
    print(f"Matcher load time:      {(t1 - t0)*1000:.2f} ms")
    print(f"Input load time:        {(t3 - t2)*1000:.2f} ms")
    print(f"Output write time:      {(t5 - t4)*1000:.2f} ms")
    print(f"Avg match latency:      {avg_match_time:.2f} ms")
    print(f"Total pipeline runtime: {total_runtime:.2f} s")

if __name__ == "__main__":
    run_timed_pipeline()
