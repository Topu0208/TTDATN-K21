import os
from collections import defaultdict

# File paths
input_file_path = "entity_list_file_wikidata_complete_all_mention"
output_file_path = "processed_entity_list_file_wikidata_complete_all_mention"

# Read input file
with open(input_file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Parse input data
data = []
for line in lines:
    parts = line.strip().split("\t")
    if len(parts) == 3:
        id_, label, count = parts[0], parts[1].replace("$002c", ","), float(parts[2])  # Use float for rate calculation
        data.append((id_, label, count))

# Step 1: Group by label and calculate total counts per label
label_totals = defaultdict(int)
for _, label, count in data:
    label_totals[label] += count

# Step 2: Calculate appearing rate for each ID within its label group
results = []
for id_, label, count in data:
    rate = count / label_totals[label]
    results.append((label, rate, id_))

# Step 3: Sort results first by label and then by ID (you can adjust the secondary sorting criteria)
results.sort(key=lambda x: (x[0], x[2]))  # Sorting by label first, then by ID

# Step 4: Write results to the output file with tab separator
with open(output_file_path, "w", encoding="utf-8") as file:
    for label, rate, id_ in results:
        file.write(f"{label}\t{rate:.2f}\t{id_}\n")

output_file_path  # Path to the generated output file
