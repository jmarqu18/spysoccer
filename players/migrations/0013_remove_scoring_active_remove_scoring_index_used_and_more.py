# Generated by Django 4.0.6 on 2022-07-16 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import players.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('players', '0012_alter_index_options_alter_index_index_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoring',
            name='active',
        ),
        migrations.RemoveField(
            model_name='scoring',
            name='index_used',
        ),
        migrations.AddField(
            model_name='scoring',
            name='rank_in_context',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Ránking en este contexto'),
        ),
        migrations.AlterField(
            model_name='index',
            name='index_name',
            field=models.CharField(max_length=6, unique=True, verbose_name='Nombre del Index'),
        ),
        migrations.CreateModel(
            name='ScoringRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de la petición')),
                ('minutes_played_min', models.IntegerField(default=0)),
                ('season_request', models.CharField(choices=[('2021-2022', '2021-2022')], default='2021-2022', max_length=50)),
                ('index_used', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='players.index', verbose_name='Index usado')),
                ('user', models.ForeignKey(null=True, on_delete=models.SET(players.models.getUser), to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Cálculo de Scoring',
                'verbose_name_plural': 'Cálculos de Scoring',
            },
        ),
        migrations.AddField(
            model_name='scoring',
            name='scoring_request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='players.scoringrequest', verbose_name='Petición de actualización de Scoring'),
        ),
    ]