# Generated by Django 4.0.6 on 2022-07-10 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0010_alter_playerfbref_fb_g_plus_a_minus_pk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerfbref',
            name='fb_player_id',
            field=models.CharField(max_length=20),
        ),
    ]