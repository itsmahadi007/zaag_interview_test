import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.cosmos.models import CosmosModel


class Command(BaseCommand):
    help = "Add Sample Data"

    def handle(self, *args, **options):
        dir_path = "web_scraper/downloaded_files"

        # Iterate over all files in the directory
        for filename in os.listdir(dir_path):
            if filename.endswith(".tsv"):
                file_path = os.path.join(dir_path, filename)

                # Read the .tsv file using pandas
                try:
                    df = pd.read_csv(file_path, sep='\t', header=0, on_bad_lines='skip')

                    # Ensure all expected columns exist, filling missing ones with None
                    expected_columns = [
                        'ID', 'Accession ID', 'GO ID', 'Class', 'Copies per Million (CPM)', 'Abundance Score',
                        'Tax ID', 'CAZy ID', 'Normalized Reads Frequency', 'Relative Abundance', 'Unique Matches',
                        'Reads Frequency', 'Unique Matches Frequency', 'Enzyme ID', 'GO Description', 'Total Matches',
                        'Pfam ID', 'Name', 'GTDB ID', 'Domain', 'GO Category'
                    ]
                    for col in expected_columns:
                        if col not in df.columns:
                            df[col] = None

                    # Replace NaN values with None
                    df = df.where(pd.notnull(df), None)

                    print("Reading Data")
                    cosmos_objects = []
                    for _, row in df.iterrows():
                        cosmos_objects.append(CosmosModel(
                            id=row.get('ID', None),
                            accession_id=row.get('Accession ID', None),
                            go_id=row.get('GO ID', None),
                            class_field=row.get('Class', None),
                            copies_per_million_cpm=float(row['Copies per Million (CPM)']) if pd.notna(
                                row['Copies per Million (CPM)']) else None,
                            abundance_score=float(row['Abundance Score']) if pd.notna(row['Abundance Score']) else None,
                            tax_id=int(row['Tax ID']) if pd.notna(row['Tax ID']) else None,
                            caz_id=row.get('CAZy ID', None),
                            normalized_reads_frequency=float(row['Normalized Reads Frequency']) if pd.notna(
                                row['Normalized Reads Frequency']) else None,
                            relative_abundance=float(row['Relative Abundance']) if pd.notna(
                                row['Relative Abundance']) else None,
                            unique_matches=float(
                                row.get('% Unique Matches') or row.get('Unique Matches', 0)) if pd.notna(
                                row.get('% Unique Matches') or row.get('Unique Matches', 0)) else None,
                            reads_frequency=float(row['Reads Frequency']) if pd.notna(row['Reads Frequency']) else None,
                            unique_matches_frequency=float(row['Unique Matches Frequency']) if pd.notna(
                                row['Unique Matches Frequency']) else None,
                            enzyme_id=row.get('Enzyme ID', None),
                            go_description=row.get('GO Description', None),
                            total_matches=float(row.get('% Total Matches') or row.get('Total Matches', 0)) if pd.notna(
                                row.get('% Total Matches') or row.get('Total Matches', 0)) else None,
                            pfam_id=row.get('Pfam ID', None),
                            name=row.get('Name', None),
                            gtdb_id=row.get('GTDB ID', None),
                            domain=row.get('Domain', None),
                            go_category=row.get('GO Category', None),
                            file_name=filename
                        ))

                    # Use bulk_create to add all records at once
                    with transaction.atomic():
                        CosmosModel.objects.bulk_create(cosmos_objects)

                except Exception as e:
                    print(f"Error reading {filename}: {e}")

        print("Data Loaded to Database")
