# Generated by Django 4.2.7 on 2023-11-15 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=100, verbose_name='name in English language')),
                ('name_lt', models.CharField(max_length=100, verbose_name='name in Lithuanian language')),
                ('description_en', models.TextField(blank=True, max_length=1000, verbose_name='description in English language')),
                ('description_lt', models.TextField(blank=True, max_length=1000, verbose_name='description in Lithuanian language')),
            ],
            options={
                'verbose_name': 'color',
                'verbose_name_plural': 'colors',
            },
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=100)),
                ('name_lt', models.CharField(max_length=100)),
                ('description_en', models.TextField(blank=True, max_length=1000)),
                ('description_lt', models.TextField(blank=True, max_length=1000)),
                ('colors', models.ManyToManyField(related_name='plants', to='gardenplaner.color', verbose_name='color')),
            ],
            options={
                'verbose_name': 'plant',
                'verbose_name_plural': 'plants',
            },
        ),
        migrations.CreateModel(
            name='PlantTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_en', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('month_lt', models.IntegerField(choices=[(1, 'Sausis'), (2, 'Vasaris'), (3, 'Kovas'), (4, 'Balandis'), (5, 'Gegužė'), (6, 'Birželis'), (7, 'Liepa'), (8, 'Rugpjūtis'), (9, 'Rugsėjis'), (10, 'Spalis'), (11, 'Lapkritis'), (12, 'Gruodis')])),
                ('first_day', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31')])),
                ('last_day', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31')])),
            ],
            options={
                'verbose_name': 'plantTime',
                'verbose_name_plural': 'plantTimes',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=100, verbose_name='project name')),
                ('public', models.BooleanField(default=False, verbose_name='public')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=100, verbose_name='name in English language')),
                ('name_lt', models.CharField(max_length=100, verbose_name='name in Lithuanian language')),
                ('description_en', models.TextField(blank=True, max_length=1000, verbose_name='description in English language')),
                ('description_lt', models.TextField(blank=True, max_length=1000, verbose_name='description in English language')),
            ],
            options={
                'verbose_name': 'type',
                'verbose_name_plural': 'types',
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='name in Lithuanian language')),
                ('lenght', models.FloatField(verbose_name='enter lenght')),
                ('width', models.FloatField(verbose_name='enter width')),
                ('public', models.BooleanField(default=False, verbose_name='public')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='gardenplaner.project', verbose_name='garden project')),
            ],
            options={
                'verbose_name': 'zone',
                'verbose_name_plural': 'zones',
            },
        ),
        migrations.CreateModel(
            name='ZonePlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blooming_period', models.CharField(blank=True, max_length=100, verbose_name='enter blooming period')),
                ('qty', models.IntegerField(verbose_name='enter quantity')),
                ('price', models.FloatField(verbose_name='enter plants price of unit')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone_plants', to='gardenplaner.color', verbose_name='color')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone_plants', to='gardenplaner.plant', verbose_name='plant')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zone_plants', to='gardenplaner.zone', verbose_name='zone')),
            ],
            options={
                'verbose_name': 'zone plant',
                'verbose_name_plural': 'zone plants',
            },
        ),
        migrations.AddField(
            model_name='plant',
            name='planting_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='gardenplaner.planttime', verbose_name='planting time'),
        ),
        migrations.AddField(
            model_name='plant',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='gardenplaner.type', verbose_name='type'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='photos/', verbose_name='add image')),
                ('season', models.CharField(choices=[('SPRING', 'SPRING'), ('SUMMER', 'SUMMER'), ('AUTUMN', 'AUTUMN'), ('WINTER', 'WINTER')], max_length=100, verbose_name='select season')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='gardenplaner.zone', verbose_name='zone')),
            ],
            options={
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
        ),
    ]
