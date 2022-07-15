# Generated by Django 4.0.6 on 2022-07-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0008_alter_playerstats_extraction_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='ca_salary',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='complete_matches_played',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='matches_as_substitute',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='mean_minutes_starts',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='mean_minutes_substitute',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='minutes_per_match',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='perc_minutes_played',
        ),
        migrations.RemoveField(
            model_name='goalkeeperstats',
            name='tm_current_value',
        ),
        migrations.RemoveField(
            model_name='playerstats',
            name='ca_salary',
        ),
        migrations.RemoveField(
            model_name='playerstats',
            name='tm_current_value',
        ),
        migrations.AddField(
            model_name='goalkeeperstats',
            name='current_value',
            field=models.IntegerField(blank=True, default=0, verbose_name='Valor de mercado'),
        ),
        migrations.AddField(
            model_name='goalkeeperstats',
            name='salary',
            field=models.IntegerField(blank=True, default=0, verbose_name='Salario anual (€)'),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='current_value',
            field=models.IntegerField(blank=True, default=0, verbose_name='Valor de mercado'),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='salary',
            field=models.IntegerField(blank=True, default=0, verbose_name='Salario anual (€)'),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='xGBuildup',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='xGBuildup_90',
            field=models.FloatField(blank=True, default=0, verbose_name='xBuildup por 90 minutos'),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='xGChain',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='playerstats',
            name='xGChain_90',
            field=models.FloatField(blank=True, default=0, verbose_name='xGChain por 90 minutos'),
        ),
    ]