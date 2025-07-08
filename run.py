from src.core.pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline(
        input_csv="src/data/test.csv",
        dataset_csv="src/data/open-source-ingredients.csv",
        output_csv="output/output.csv"
    )
