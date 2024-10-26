import os
import pandas as pd

dir_path = "downloaded_files"

unique_headers = set()

for filename in os.listdir(dir_path):
    if filename.endswith(".tsv"):
        file_path = os.path.join(dir_path, filename)

        try:
            df = pd.read_csv(file_path, sep='\t')
      
            unique_headers.update(df.columns)
        except Exception as e:
            print(f"Error reading {filename}: {e}")


print("Unique headers found across all files:")
print(unique_headers)
print(f"Length of unique headers: {len(unique_headers)}")
# for header in unique_headers:
#     print(header)
