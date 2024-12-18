# Generated by Django 4.2 on 2024-10-27 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosmos", "0002_datamodel_results_rootsample_subsample_taxonomy_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="datamodel",
            name="tax_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="results",
            unique_together={("sub_sample", "name")},
        ),
        migrations.AlterUniqueTogether(
            name="subsample",
            unique_together={("name", "root_sample")},
        ),
        migrations.AlterUniqueTogether(
            name="taxonomy",
            unique_together={("result_of", "name")},
        ),
    ]
