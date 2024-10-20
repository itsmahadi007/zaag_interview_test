# Generated by Django 4.2 on 2024-10-20 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CosmosModel",
            fields=[
                ("primary_key", models.AutoField(primary_key=True, serialize=False)),
                ("id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "accession_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("go_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "class_field",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("copies_per_million_cpm", models.FloatField(blank=True, null=True)),
                ("abundance_score", models.FloatField(blank=True, null=True)),
                ("tax_id", models.IntegerField(blank=True, null=True)),
                ("caz_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "normalized_reads_frequency",
                    models.FloatField(blank=True, null=True),
                ),
                ("relative_abundance", models.FloatField(blank=True, null=True)),
                ("unique_matches", models.FloatField(blank=True, null=True)),
                ("reads_frequency", models.FloatField(blank=True, null=True)),
                ("unique_matches_frequency", models.FloatField(blank=True, null=True)),
                ("enzyme_id", models.CharField(blank=True, max_length=255, null=True)),
                ("go_description", models.TextField(blank=True, null=True)),
                ("total_matches", models.FloatField(blank=True, null=True)),
                ("pfam_id", models.CharField(blank=True, max_length=255, null=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("gtdb_id", models.CharField(blank=True, max_length=255, null=True)),
                ("domain", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "go_category",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("file_name", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
