# Generated by Django 4.2.7 on 2023-11-20 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gardenplaner', '0002_project_description_zone_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='add image'),
        ),
    ]