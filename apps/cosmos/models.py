from django.db import models



class RootSample(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
class SubSample(models.Model):
    name = models.CharField(max_length=255)
    root_sample = models.ForeignKey(RootSample, on_delete=models.CASCADE, related_name='sub_samples')

class Results(models.Model):
    sub_sample = models.ForeignKey(SubSample, on_delete=models.CASCADE, related_name='results')
    name = models.CharField(max_length=255)
    
class Taxonomy(models.Model):
    result_of = models.ForeignKey(Results, on_delete=models.CASCADE, limit_choices_to={'name': 'Bacteria'}, related_name='taxonomy')
    name = models.CharField(max_length=255)
    

class DataModel(models.Model):
    primary_key = models.AutoField(primary_key=True)
    result_of = models.ForeignKey(Results, on_delete=models.CASCADE, related_name='data_models', null=True, blank=True)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='data_models', null=True, blank=True)  
    
    id = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    accession_id = models.CharField(max_length=255, null=True, blank=True)
    go_id = models.CharField(max_length=255, null=True, blank=True)
    class_field = models.CharField(max_length=255, null=True,
                                   blank=True)
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

    class Meta:
        ordering = ['primary_key']
