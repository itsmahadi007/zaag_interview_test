import os
import csv
from django.core.management.base import BaseCommand

from apps.cosmos.models import DataModel, Results, RootSample, SubSample, Taxonomy
from django.db import transaction
import pandas as pd


class Command(BaseCommand):
    help = "Load Cosmos Data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_sample_objects = {}
        self.sub_sample_objects = {}
        self.result_objects = {}
        self.taxonomy_objects = {}
        self.data_models = []
        self.expected_columns = [
            "ID",
            "Accession ID",
            "GO ID",
            "Class",
            "Copies per Million (CPM)",
            "Abundance Score",
            "Tax ID",
            "CAZy ID",
            "Normalized Reads Frequency",
            "Relative Abundance",
            "Unique Matches",
            "Reads Frequency",
            "Unique Matches Frequency",
            "Enzyme ID",
            "GO Description",
            "Total Matches",
            "Pfam ID",
            "Name",
            "GTDB ID",
            "Domain",
            "GO Category",
        ]

    def split_filename(self, filename):
        parts = filename.split("__")
        root_sample = parts[0]
        subsample = parts[1]
        result = parts[2]
        taxonomy = None
        datetime = parts[-1].split(".")[0]  # Remove file extension

        if result == "Bacteria" and len(parts) == 5:
            taxonomy = parts[3]

        return root_sample, subsample, result, taxonomy, datetime

    def get_instance_from_filename(self, filename):
        root_sample, subsample, result, taxonomy, datetime = self.split_filename(
            filename
        )

        if root_sample not in self.root_sample_objects:
            self.root_sample_objects[root_sample], _ = RootSample.objects.get_or_create(
                name=root_sample
            )
        root_sample_obj = self.root_sample_objects[root_sample]

        if subsample not in self.sub_sample_objects:
            self.sub_sample_objects[subsample], _ = SubSample.objects.get_or_create(
                name=subsample, root_sample=root_sample_obj
            )
        sub_sample_obj = self.sub_sample_objects[subsample]

        if result not in self.result_objects:
            self.result_objects[result], _ = Results.objects.get_or_create(
                name=result, sub_sample=sub_sample_obj
            )
        result_obj = self.result_objects[result]

        taxonomy_obj = None
        if taxonomy:
            if taxonomy not in self.taxonomy_objects:
                self.taxonomy_objects[taxonomy], _ = Taxonomy.objects.get_or_create(
                    result_of=result_obj, name=taxonomy
                )
            taxonomy_obj = self.taxonomy_objects[taxonomy]

        return root_sample_obj, sub_sample_obj, result_obj, taxonomy_obj

    def handle(self, *args, **options):
        dir_path = "web_scraper/downloads"

        for root, dirs, files in os.walk(dir_path):
            for filename in files:
                try:
                    print(f"Processing file: {filename}")
                    if filename.endswith(".tsv"):
                        file_path = os.path.join(root, filename)
                        with open(file_path, "r") as file:
                            reader = csv.DictReader(file, delimiter="\t")
                            if not reader.fieldnames:
                                # Handle empty file
                                self.create_empty_data_model(filename)
                            else:
                                for row in reader:
                                    self.create_data_model_from_row(row, filename)
                except Exception as e:
                    print(f"Error processing file {filename}: {str(e)}")
                    continue

        with transaction.atomic():
            print(f"Adding {len(self.data_models)} rows to data model with a single query")
            DataModel.objects.bulk_create(self.data_models)
            print("Done!")

    def create_empty_data_model(self, filename):
        # Determine whether to use result_of or taxonomy based on filename
        root_sample_obj, sub_sample_obj, result_obj, taxonomy_obj = (
            self.get_instance_from_filename(filename)
        )
        if taxonomy_obj:
            self.data_models.append(
                DataModel(result_of=result_obj, taxonomy=taxonomy_obj)
            )
        else:
            self.data_models.append(DataModel(result_of=result_obj))

    def create_data_model_from_row(self, row, filename):
        print(f"Adding row to data model: {filename}")
        root_sample_obj, sub_sample_obj, result_obj, taxonomy_obj = (
            self.get_instance_from_filename(filename)
        )
        
        for col in self.expected_columns:
            if col not in row.keys():
                row[col] = None

        self.data_models.append(
            DataModel(
                id=row.get("ID", None),
                result_of=result_obj,
                taxonomy=taxonomy_obj,
                accession_id=row.get("Accession ID", None),
                go_id=row.get("GO ID", None),
                class_field=row.get("Class", None),
                copies_per_million_cpm=(
                    float(row["Copies per Million (CPM)"])
                    if pd.notna(row["Copies per Million (CPM)"])
                    else None
                ),
                abundance_score=(
                    float(row["Abundance Score"])
                    if pd.notna(row["Abundance Score"])
                    else None
                ),
                tax_id=str(row["Tax ID"]) if pd.notna(row["Tax ID"]) else None,
                caz_id=row.get("CAZy ID", None),
                normalized_reads_frequency=(
                    float(row["Normalized Reads Frequency"])
                    if pd.notna(row["Normalized Reads Frequency"])
                    else None
                ),
                relative_abundance=(
                    float(row["Relative Abundance"])
                    if pd.notna(row["Relative Abundance"])
                    else None
                ),
                unique_matches=(
                    float(row.get("% Unique Matches") or row.get("Unique Matches", 0))
                    if pd.notna(
                        row.get("% Unique Matches") or row.get("Unique Matches", 0)
                    )
                    else None
                ),
                reads_frequency=(
                    float(row["Reads Frequency"])
                    if pd.notna(row["Reads Frequency"])
                    else None
                ),
                unique_matches_frequency=(
                    float(row["Unique Matches Frequency"])
                    if pd.notna(row["Unique Matches Frequency"])
                    else None
                ),
                enzyme_id=row.get("Enzyme ID", None),
                go_description=row.get("GO Description", None),
                total_matches=(
                    float(row.get("% Total Matches") or row.get("Total Matches", 0))
                    if pd.notna(
                        row.get("% Total Matches") or row.get("Total Matches", 0)
                    )
                    else None
                ),
                pfam_id=row.get("Pfam ID", None),
                name=row.get("Name", None),
                gtdb_id=row.get("GTDB ID", None),
                domain=row.get("Domain", None),
                go_category=row.get("GO Category", None),
                file_name=filename,
            )
        )
