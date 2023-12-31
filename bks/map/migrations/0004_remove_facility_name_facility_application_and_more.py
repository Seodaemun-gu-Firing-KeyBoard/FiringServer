# Generated by Django 4.2.4 on 2023-08-15 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_delete_facilitytest_remove_facility_application_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facility',
            name='name',
        ),
        migrations.AddField(
            model_name='facility',
            name='application',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='call',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='cancel',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='fee',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='location',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='reception',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='recruit',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='reserve',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='select',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='target',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facility',
            name='use',
            field=models.TextField(blank=True, null=True),
        ),
    ]
