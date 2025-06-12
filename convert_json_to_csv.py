# This script converts JSON to CSV
import pandas as pd
import json
import sys

# Read JSON file from input
with open(sys.argv[1], 'r') as json_file:
    data = json.load(json_file)

# Convert JSON to DataFrame
if isinstance(data, list):
    df = pd.DataFrame(data)
else:
    df = pd.DataFrame([data])

# Convert DataFrame to CSV
csv_path = sys.argv[2]
df.to_csv(csv_path, index=False)
