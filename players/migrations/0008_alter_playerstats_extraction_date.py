# Generated by Django 4.0.6 on 2022-07-14 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0007_playerstats_goalkeeperstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerstats',
            name='extraction_date',
            field=models.DateTimeField(verbose_name='Fecha de extracción'),
        ),
    ]
