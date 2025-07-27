
# 🌱 EcoMatch - Intelligent Product-to-Carbon Matching

EcoMatch is a semantic product matching system designed to map noisy product descriptions (e.g. from receipts) to structured ingredient data and return their carbon impact rating.

---

## 🚀 Pipeline Overview

### 1. **Preprocessing (One-time Setup)**

This step cleans, embeds, and indexes the ingredient reference dataset.

- Cleans product names using regex-based normalization
- Generates semantic embeddings using Sentence-BERT
- Saves:
  - `product_index.parquet`: Cleaned product dataset
  - `product_embeddings.npy`: NumPy array of embedding vectors
  - `faiss_index.bin`: Precomputed FAISS index for fast similarity search

Run:

```bash
python preprocess.py
```

---

### 2. **Matching Pipeline (For New Inputs)**

This runs the matching process for a given input list (`test.csv`) and produces `output.csv`.

For each product:
- Cleans the name
- Embeds the input using Sentence-BERT
- Searches top-K similar products using FAISS
- Re-ranks with a fuzzy-semantic scoring blend:  
  `score = α × semantic + (1 - α) × fuzzy_ratio`
- Returns: `input_product`, `matched_product`, `carbon_rating`

Run:

```bash
python run.py
```

The script logs:
- Matcher load time
- Input read time
- Per-product match latency
- Output write time
- Total runtime

---

### 3. **Evaluation**

To check how accurate the matches are:

```bash
python evaluate.py
```

Returns overall accuracy of carbon rating matching.

---

## 📁 Directory Structure

```
eco-match-challenge/
├── src/
│   ├── run.py                 # Main match runner
│   ├── preprocess.py          # Preprocessing + index builder
│   ├── evaluate.py            # Evaluation script
│   ├── core/
│   │   ├── matching.py        # FAISS + fuzzy matching logic
│   │   ├── pipeline.py        # Pipeline orchestrator
│   │   ├── embedding.py       # Sentence-BERT embedder
│   │   ├── cleaning.py        # Regex-based cleaner
│   │   ├── io.py              # Parquet/NPY file utils
│   └── data/
│       ├── open-source-ingredients.csv
│       ├── test.csv
│       └── ground-truth.csv
├── data/processed/
│   ├── product_index.parquet
│   ├── product_embeddings.npy
│   └── faiss_index.bin
└── output/
    └── output.csv
```

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Required:
- `sentence-transformers`
- `faiss-cpu`
- `thefuzz[speedup]`
- `numpy`, `pandas`, `pyarrow`

---

## 🧠 Key Concepts

- **FAISS**: High-speed vector similarity search over embeddings
- **Sentence-BERT**: Converts names into semantic embeddings
- **Fuzzy Re-ranking**: Improves robustness to text noise (e.g., brand names, order)

---

## 🔍 Example Input → Output

### Input (test.csv):

```
product_name
"Ben & Jerry's Chocolate Fudge Ice Cream 500ml"
"Organic Whole Milk 2L"
```

### Output (output.csv):

```
input_product,matched_product,carbon_rating
"Ben & Jerry's...",Ice Cream,C
"Organic Whole Milk...",Whole Milk,B
```

---

## 📈 Performance Notes

- FAISS is pre-indexed → no recomputation at runtime
- Pipeline prints timing stats per step
- Average match latency ~11-16ms on CPU

---

## 🛠️ Enhancement Ideas

- Add domain-aware synonym based token replacements logic during cleaning
- Going with VectoDB(chromaDB,Qdrant)instead of Numpy embedding storage while still using FAISS as backend
- Smart Index Refresh(automating--- tracking changes in open-source-ingredients.csv → appending new rows(clean→embed→vectors) avoiding full recomputes
- Add caching layers such as Embedder Cache (to avoid redundant Sentence-BERT encoding) and FAISS Search Result Cache (to skip repeated top-K lookups for similar queries)
- Switch to GPU FAISS (`faiss-gpu`)
- Add REST API with FastAPI/Flask for real-time querying
- Plug in OCR layer from receipt image

---
