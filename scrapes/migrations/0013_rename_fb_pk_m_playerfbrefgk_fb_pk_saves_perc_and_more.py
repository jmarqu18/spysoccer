# Generated by Django 4.0.6 on 2022-07-11 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0012_alter_playerfbrefgk_fb_player_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playerfbrefgk',
            old_name='fb_PK_m',
            new_name='fb_PK_saves_perc',
        ),
        migrations.RenameField(
            model_name='playerfbrefgk',
            old_name='fb_PSxG_plus_vs_minus',
            new_name='fb_PSxG_dif',
        ),
    ]