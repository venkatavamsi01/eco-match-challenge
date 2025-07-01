# read flags from input
import argparse
import csv


parser = argparse.ArgumentParser()
parser.add_argument('--output', type=str, default='data/output.csv')
args = parser.parse_args()


# read ground truth
truth = {}

with open('data/ground-truth.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        input, matched_product, carbon_rating = row
        truth[input] = carbon_rating


output = {}
with open(args.output, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        input, matched_product, carbon_rating = row
        output[input] = carbon_rating

# calculate accuracy
correct = 0
for input in truth:
    if output[input] == truth[input]:
        correct += 1

accuracy = (correct / len(truth))*100
print(f"Accuracy: {accuracy:.2f}%")