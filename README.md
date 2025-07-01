## 💡 EcoMatch - Product Matching System

### Overview

In this assignment, you will build **EcoMatch**, a product matching system that takes a product name as input and finds the closest match from a pool of food products, along with its carbon rating. The goal is to evaluate your ability to design a performant, scalable matching solution with a well-justified approach.

Your solution must:

- Handle unclean product names by cleaning and normalizing inputs.
- Accurately match to the closest dataset product.
- Be well-documented, modular, and scalable.

---

### Challenge Brief

You will build a system with the following capabilities:

- **I/O:**
    - Accept an `input.csv` file containing a list of product names to match.
    - Produce an `output.csv` file with the matching results.
- **Dataset Flexibility:**
    - Design your system so that the dataset of known products can be **easily replaced or extended**, for example by swapping the CSV or spreadsheet file, **without requiring major code changes**

**Technical Stack**:

- You are free to use technical stack of your choice, for example it can be
    - ML model
    - AI wrapper
    - Algorithm

---

### User Story

1. In a real-world scenario, an external service would query the system by sending a product name through an API call.
2. The system would identify the closest match for the given product from the pool of products in the dataset and respond with the matched product and its carbon rating.
3. **For this assignment**, instead of implementing an API, the system should simulate API calls by:
    1. Accepting an `input.csv` file containing a list of product names to match.
    2. Producing an `output.csv` file containing:
        - `input_product`: original product name from the input
        - `matched_product`: closest matched product name from the dataset
        - `carbon_rating`: carbon rating of the matched product
4. The response time for matching each product should be fast.

---

### Files & Datasets

**Carbon score dataset**

https://docs.google.com/spreadsheets/d/1x2pYXt0ZZ5j8-69CBK8OOWparaPt2r2gR94mRF-9Dg8/edit?usp=sharing

- Sheet description
    
    
    | field | description |
    | --- | --- |
    | `name` | Original product name in the dataset |
    | `clean_name` | Preprocessed and cleaned version of `name`  |
    | `carbon_rating` | Carbon impact rating (e.g., A/B/C/D)C |
    | `co2e` | Estimated CO₂ emissions in kg per kg/litre |
    | `lca_farm`, `lca_processing`, `lca_packaging`, `lca_transport`, `lca_retail`, `lca_food_waste` | Life-cycle assessment components in kg CO₂ for each stage |
    | `source` | Source reference for the carbon data |

- test.csv
- truth.csv
- evaluate.py

---

### How to Test Your System?

**Example test and output files**

test.csv

```
product_name
"Ben & Jerry's Chocolate Fudge Ice Cream 500ml"
"Organic Whole Milk 2L"
```

output.csv

```
input_product,matched_product,carbon_rating
"Ben & Jerry's Chocolate Fudge Ice Cream 500ml","Ice Cream","C"
"Organic Whole Milk 2L","Whole Milk","B"
```

**Test instructions:**

1. Once your system produces `output.csv`, you can evaluate its accuracy against the ground truth provided in `ground-truth.csv` using the included evaluation script:
    
    ```bash
    cd src
    python evaluate.py --output output.csv
    ```
    
2. The script will print metrics such as:
    - **Accuracy score**: percentage of exact matches with the ground truth.
3. Your submission should aim for high accuracy while ensuring average response time is fast.

---

### Considerations

1. **Input Cleaning :** The input names can be unclean with brand names or product quantities. Your system **must** handle noisy product names (e.g., brands, volumes) through text cleaning or normalization before matching.

---

### Submission Guidelines

1. **GitHub Repository**:
    - Create a GitHub repository named `eco-match-challenge`.
    - Commit all source code, and documentation to this repository.
    - A `README.md` file with instructions mentioned below
2. **Documentation in README.md**:
    - **Setup Instructions**: Detailed steps to install dependencies, configure environment variables, and start the application.
    - **Run Instructions**: Information on accessing the application locally, including URLs.
    - **Simple Architecture  Diagram**: Include a simple flow diagram or schematic in your README that illustrates how your system processes inputs and produces outputs.
        - Your diagram should highlight the main processing steps in your pipeline so reviewers can quickly understand your approach.
        - For example:
    
    ```
    Input.csv → Input Cleaning → Vectorization / Embedding → Nearest Neighbor Search → Match Selection → Output.csv
    ```
    

Additional Pointers:

1. **Scalability**: In the documentation, include how system behaves when the pool of products are increased from thousands to millions. Such as any delay in response, expensive pre-processing
2. **Submission Format**: Please share a GitHub repository link to submit your final project. Include any supplementary files or documentation you find useful for reviewers.

---

**Questions**: For questions about the challenge, role, or Reewild, reach out anytime.

Please send an email with your GitHub repository and your resume to **rithin.chalumuri@reewild.com**. Looking forward to seeing the hack —have fun with it! 🌱

---

### Evaluation Criteria

- **Accuracy:** How closely does the system’s `matched_product` align with the expected matches in `truth.csv`?
- **Latency:** What is the average time taken to process each product name? Submissions should keep response time fast.
- **Scalability:** Articulate potential bottlenecks and how your solution would scale to millions of products. Considering pre-processing, indexing, and memory usage
- **Code Quality:** Is the code clean, modular, and well-documented?
- **Documentation:** Does the README clearly explain setup, assumptions, architecture, and enhancement proposals?

---

### Suggested GitHub README.md Structure

Please add and remove sections you think are appropriate. This is just a rough example. 

```jsx

# 🍃 EcoMatch - Product Matching System

## 📜 Overview
**EcoMatch** is a product matching system designed to help users understand the environmental impact of the food products they consume. By providing a product name, the system identifies the closest matching product from a dataset and outputs its carbon rating. This project demonstrates your ability to design an efficient, low-latency matching pipeline, while considering trade-offs and scalability.

---

## 🔧 Tech Stack
You are free to choose any stack you like, such as:
- **ML/AI**: Pre-trained embeddings (e.g., Sentence-BERT), vector search libraries (e.g., FAISS, Annoy)
- **Programming Language**: Python, Node.js, or others
- **Data Handling**: Pandas, SQL, or in-memory dictionaries
- **Optional**: FastAPI or Flask for API integration (if you wish to extend)

---

## 🚀 Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/eco-match-challenge.git
   cd eco-match-challenge
	```
2. **Install Dependencies**  
   Run the following commands depending on your tech stack:
   ```bash
   pip install -r requirements.txt   # if using Python
   ```

## 🚀 Setup Instructions

3. **Download Dataset**  
   - Open the [carbon score dataset](https://docs.google.com/spreadsheets/d/1x2pYXt0ZZ5j8-69CBK8OOWparaPt2r2gR94mRF-9Dg8/edit?usp=sharing) and export it as `dataset.csv`.
   - Place `dataset.csv` in your project directory so your system can read from it during matching.

4. **Run the Application**
   Run your matching system by specifying the input CSV (products to match), the dataset, and the desired output file:
   ```bash
   python run_matching.py --input test.csv --output output.csv --dataset dataset.csv
	```
5. **Testing & Evaluation**  
   After generating your `output.csv`, evaluate your system’s accuracy and performance against the ground truth:
   ```bash
   python evaluate.py --truth truth.csv --pred output.csv
	```
---

## 📁 File Descriptions
- dataset.csv: Contains product pool with carbon scores and detailed LCA breakdowns.
- test.csv: List of input product names to match.
- truth.csv: Ground truth for evaluation.
- evaluate.py: Script to calculate accuracy and latency.
- run_matching.py: Your matching system entry point.

## 🌱 Architecture
 A simple matching pipeline might look like this:
```
	Input.csv → Input Cleaning → Vectorization/Embedding → Nearest Neighbor Search → Match Selection → Output.csv
```

```

---

[]()
