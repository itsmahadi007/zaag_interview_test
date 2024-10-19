# Generated by Django 4.2 on 2024-10-19 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosmos", "0002_cosmosmodel_file_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cosmosmodel",
            old_name="reads",
            new_name="reads_frequency",
        ),
        migrations.RemoveField(
            model_name="cosmosmodel",
            name="file_name",
        ),
        migrations.AddField(
            model_name="cosmosmodel",
            name="unique_matches_frequency",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="cosmosmodel",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]