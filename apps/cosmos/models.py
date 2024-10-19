from django.db import models


# Create your models here.

class CosmosModel(models.Model):
    normalized_reads_frequency = models.FloatField(null=True, blank=True)
    tax_id = models.IntegerField(null=True, blank=True)
    relative_abundance = models.FloatField(null=True, blank=True)
    unique_matches_frequency = models.FloatField(null=True, blank=True)
    abundance_score = models.FloatField(null=True, blank=True)
    reads_frequency = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f" {self.id} - {self.name} - {self.file_name}"
