# Generated by Django 4.2.4 on 2023-08-15 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_remove_facility_name_facility_application_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
