# Generated by Django 4.0.6 on 2022-07-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playertransfermarkt',
            options={'verbose_name': 'Player data from Transfermarkt', 'verbose_name_plural': 'Players data from Transfermarkt'},
        ),
        migrations.AlterField(
            model_name='scrapejob',
            name='state',
            field=models.CharField(choices=[('OK', 'Completado'), ('KO', 'Con errores')], default='OK', max_length=20),
        ),
    ]