import os
import pandas as pd

# Folder containing .tsv files
dir_path = "downloaded_files"

# Set to store unique headers
unique_headers = set()

# Iterate over all files in the directory
for filename in os.listdir(dir_path):
    if filename.endswith(".tsv"):
        file_path = os.path.join(dir_path, filename)

        # Read the .tsv file using pandas
        try:
            df = pd.read_csv(file_path, sep='\t')
            # Update the set with headers from the current file
            unique_headers.update(df.columns)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

# Print all unique headers
print("Unique headers found across all files:")
print(unique_headers)
print(f"Length of unique headers: {len(unique_headers)}")
# for header in unique_headers:
#     print(header)
