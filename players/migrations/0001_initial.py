# Generated by Django 4.0.6 on 2022-07-12 11:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('index_name', models.CharField(max_length=50, verbose_name='Nombre del Index')),
                ('description', models.TextField(blank=True, verbose_name='Descripción corta')),
                ('position_norm', models.CharField(max_length=30, verbose_name='Posición normalizada')),
                ('index_data', models.JSONField(verbose_name='Métricas y pesos del Index')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('updated_date', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Index',
                'verbose_name_plural': 'Indexes',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120, verbose_name='Nombre del jugador')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('citizenship', models.CharField(blank=True, max_length=80, verbose_name='País de origen')),
                ('height', models.FloatField(blank=True, verbose_name='Altura')),
                ('foot', models.CharField(blank=True, max_length=10, verbose_name='Pie')),
                ('position', models.CharField(max_length=50, verbose_name='Posición')),
                ('position_norm', models.CharField(max_length=30, verbose_name='Posición normalizada')),
                ('id_fbref', models.CharField(blank=True, max_length=30)),
                ('id_understat', models.IntegerField(blank=True)),
                ('id_transfermarkt', models.IntegerField(blank=True)),
                ('id_capology', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'verbose_name': 'Jugador',
                'verbose_name_plural': 'Jugadores',
            },
        ),
        migrations.CreateModel(
            name='Scoring',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scoring', models.FloatField(verbose_name='Scoring')),
                ('calculate_date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha del cálculo')),
                ('active', models.BooleanField(default=True)),
                ('index_used', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='players.index', verbose_name='Index usado')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.player', verbose_name='Jugador')),
            ],
            options={
                'verbose_name': 'Scoring',
                'verbose_name_plural': 'Scorings',
            },
        ),
    ]
