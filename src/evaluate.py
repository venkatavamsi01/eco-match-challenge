import argparse
import csv

# Read CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, default='data/output.csv', help='Path to model output CSV')
parser.add_argument('--truth', type=str, default='src/data/ground-truth.csv', help='Path to ground truth CSV')
args = parser.parse_args()

# Load ground truth
truth = {}
with open(args.truth, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        input, matched_product, carbon_rating = row
        truth[input] = carbon_rating

# Load output
output = {}
with open(args.output, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        input, matched_product, carbon_rating = row
        output[input] = carbon_rating

# Calculate accuracy
correct = 0
for input in truth:
    if output.get(input) == truth[input]:
        correct += 1

accuracy = (correct / len(truth)) * 100
print(f"Accuracy: {accuracy:.2f}%")
