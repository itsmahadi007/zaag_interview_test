# Generated by Django 4.2 on 2024-10-19 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosmos", "0003_rename_reads_cosmosmodel_reads_frequency_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cosmosmodel",
            name="file_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
