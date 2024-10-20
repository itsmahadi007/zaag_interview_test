from django.db import models


class CosmosModel(models.Model):
    primary_key = models.AutoField(primary_key=True)
    id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    accession_id = models.CharField(max_length=255, null=True, blank=True)
    go_id = models.CharField(max_length=255, null=True, blank=True)
    class_field = models.CharField(max_length=255, null=True,
                                   blank=True)  # 'Class' renamed to avoid conflict with Python keyword
    copies_per_million_cpm = models.FloatField(null=True, blank=True)
    abundance_score = models.FloatField(null=True, blank=True)
    tax_id = models.IntegerField(null=True, blank=True)
    caz_id = models.CharField(max_length=255, null=True, blank=True)
    normalized_reads_frequency = models.FloatField(null=True, blank=True)
    relative_abundance = models.FloatField(null=True, blank=True)
    unique_matches = models.FloatField(null=True, blank=True)  # '% Unique Matches' renamed
    reads_frequency = models.FloatField(null=True, blank=True)
    unique_matches_frequency = models.FloatField(null=True, blank=True)
    enzyme_id = models.CharField(max_length=255, null=True, blank=True)
    go_description = models.TextField(null=True, blank=True)
    total_matches = models.FloatField(null=True, blank=True)  # '% Total Matches' renamed
    pfam_id = models.CharField(max_length=255, null=True, blank=True)
    gtdb_id = models.CharField(max_length=255, null=True, blank=True)
    domain = models.CharField(max_length=255, null=True, blank=True)
    go_category = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f" {self.id} - {self.name} - {self.file_name}"
