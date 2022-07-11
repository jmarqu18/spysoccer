# Generated by Django 4.0.6 on 2022-07-11 16:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeJob',
            fields=[
                ('scrape_job_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de creación')),
                ('mode', models.CharField(max_length=20, verbose_name='Modo')),
                ('origin', models.CharField(choices=[('FB', 'FB'), ('FG', 'FG'), ('US', 'US'), ('TM', 'TM'), ('CA', 'CA')], default='FB', max_length=2, verbose_name='Origen')),
                ('scraped_from', models.CharField(max_length=50, verbose_name='Extraido de')),
                ('season_from', models.CharField(max_length=30, verbose_name='Temporada')),
                ('state', models.CharField(choices=[('OK', 'Completado'), ('KO', 'Con errores'), ('IN', 'En proceso')], default='IN', max_length=20, verbose_name='Estado')),
                ('number_errors', models.IntegerField(blank=True, default=0, verbose_name='Errores')),
                ('completed_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de finalización')),
            ],
            options={
                'verbose_name': 'Web Scraping Job',
                'verbose_name_plural': 'Web Scraping Jobs',
            },
        ),
        migrations.CreateModel(
            name='PlayerUnderstat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('us_player_id', models.IntegerField(blank=True, default=0)),
                ('us_player_name', models.CharField(max_length=250)),
                ('us_position', models.CharField(max_length=10)),
                ('us_team', models.CharField(max_length=150)),
                ('us_season', models.CharField(max_length=30)),
                ('us_comp', models.CharField(max_length=50)),
                ('us_key_passes', models.IntegerField(blank=True, default=0)),
                ('us_xGChain', models.FloatField(blank=True, default=0)),
                ('us_xGBuildup', models.FloatField(blank=True, default=0)),
                ('us_key_passes_90', models.FloatField(blank=True, default=0)),
                ('us_xGChain_90', models.FloatField(blank=True, default=0)),
                ('us_xGBuildup_90', models.FloatField(blank=True, default=0)),
                ('created_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('scrape_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapes.scrapejob')),
            ],
            options={
                'verbose_name': 'Datos de jugador de Understat',
                'verbose_name_plural': 'Datos de jugadores de Understat',
            },
        ),
        migrations.CreateModel(
            name='PlayerTransfermarkt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tm_player_id', models.IntegerField()),
                ('tm_player_name', models.CharField(max_length=120)),
                ('tm_comp', models.CharField(max_length=50)),
                ('tm_player_image_url', models.URLField()),
                ('tm_current_value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('tm_birthdate', models.DateField(blank=True, null=True)),
                ('tm_yearbirthdate', models.CharField(blank=True, max_length=4)),
                ('tm_citizenship', models.CharField(blank=True, max_length=100)),
                ('tm_position', models.CharField(blank=True, max_length=60)),
                ('tm_height', models.CharField(blank=True, max_length=50)),
                ('tm_foot', models.CharField(blank=True, max_length=20)),
                ('tm_current_club', models.CharField(max_length=100)),
                ('tm_date_joined', models.DateField(blank=True, null=True)),
                ('tm_contract_expires', models.DateField(blank=True, null=True)),
                ('created_data', models.DateTimeField(auto_now=True)),
                ('scrape_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapes.scrapejob')),
            ],
            options={
                'verbose_name': 'Datos de jugador de Transfermarkt',
                'verbose_name_plural': 'Datos de jugadores Transfermarkt',
            },
        ),
        migrations.CreateModel(
            name='PlayerFbrefGK',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fb_player_id', models.CharField(max_length=30)),
                ('fb_player_name', models.CharField(max_length=120)),
                ('fb_season', models.CharField(max_length=30)),
                ('fb_nation', models.CharField(max_length=3)),
                ('fb_pos', models.CharField(max_length=10, verbose_name='fb_position')),
                ('fb_team', models.CharField(blank=True, max_length=50)),
                ('fb_comp', models.CharField(max_length=50, verbose_name='fb_competition')),
                ('fb_born', models.CharField(blank=True, max_length=4)),
                ('fb_playing_time_MP', models.IntegerField(blank=True, default=0)),
                ('fb_playing_time_starts', models.IntegerField(blank=True, default=0)),
                ('fb_playing_time_min', models.IntegerField(blank=True, default=0)),
                ('fb_playing_time_90s', models.FloatField(blank=True, default=0)),
                ('fb_Gls', models.IntegerField(blank=True, default=0)),
                ('fb_Ast', models.IntegerField(blank=True, default=0)),
                ('fb_G_minus_PK', models.IntegerField(blank=True, default=0)),
                ('fb_PK', models.IntegerField(blank=True, default=0)),
                ('fb_PKatt', models.IntegerField(blank=True, default=0)),
                ('fb_CrdY', models.IntegerField(blank=True, default=0)),
                ('fb_CrdR', models.IntegerField(blank=True, default=0)),
                ('fb_Gls_90', models.FloatField(blank=True, default=0)),
                ('fb_Ast_90', models.FloatField(blank=True, default=0)),
                ('fb_G_plus_A_90', models.FloatField(blank=True, default=0)),
                ('fb_G_plus_A_minus_PK', models.FloatField(blank=True, default=0)),
                ('fb_xG', models.FloatField(blank=True, default=0)),
                ('fb_npxG', models.FloatField(blank=True, default=0)),
                ('fb_xA', models.FloatField(blank=True, default=0)),
                ('fb_npxG_plus_xA', models.FloatField(blank=True, default=0)),
                ('fb_xG_90', models.FloatField(blank=True, default=0)),
                ('fb_xA_90', models.FloatField(blank=True, default=0)),
                ('fb_xG_plus_xA_90', models.FloatField(blank=True, default=0)),
                ('fb_npxG_90', models.FloatField(blank=True, default=0)),
                ('fb_npxG_plus_xA_90', models.FloatField(blank=True, default=0)),
                ('fb_GA', models.IntegerField(blank=True, default=0)),
                ('fb_GA_90', models.FloatField(blank=True, default=0)),
                ('fb_SoTA', models.IntegerField(blank=True, default=0)),
                ('fb_saves', models.IntegerField(blank=True, default=0)),
                ('fb_save_perc', models.FloatField(blank=True, default=0)),
                ('fb_W', models.IntegerField(blank=True, default=0)),
                ('fb_D', models.IntegerField(blank=True, default=0)),
                ('fb_L', models.IntegerField(blank=True, default=0)),
                ('fb_CS', models.IntegerField(blank=True, default=0)),
                ('fb_CS_perc', models.FloatField(blank=True, default=0)),
                ('fb_PK_against', models.IntegerField(blank=True, default=0)),
                ('fb_PK_saves', models.IntegerField(blank=True, default=0)),
                ('fb_PK_saves_perc', models.FloatField(blank=True, default=0)),
                ('fb_PSxG', models.FloatField(blank=True, default=0)),
                ('fb_PSxG_vs_SoT', models.FloatField(blank=True, default=0)),
                ('fb_PSxG_dif', models.FloatField(blank=True, default=0)),
                ('fb_Launched_Cmp', models.IntegerField(blank=True, default=0)),
                ('fb_Launched_Att', models.IntegerField(blank=True, default=0)),
                ('fb_Launched_Cmp_perc', models.FloatField(blank=True, default=0)),
                ('fb_Passes_Att', models.IntegerField(blank=True, default=0)),
                ('fb_Passes_Thr', models.IntegerField(blank=True, default=0)),
                ('fb_Passes_Launch_perc', models.FloatField(blank=True, default=0)),
                ('fb_Passes_AvgLen', models.FloatField(blank=True, default=0)),
                ('fb_Goal_Kicks_Att', models.IntegerField(blank=True, default=0)),
                ('fb_Goal_Kicks_Launch_perc', models.FloatField(blank=True, default=0)),
                ('fb_Goal_Kicks_AvgLen', models.FloatField(blank=True, default=0)),
                ('fb_Crosses_Opp', models.IntegerField(blank=True, default=0)),
                ('fb_Crosses_Stp', models.IntegerField(blank=True, default=0)),
                ('fb_Crosses_Stp_perc', models.FloatField(blank=True, default=0)),
                ('fb_Sweeper_OPA', models.FloatField(blank=True, default=0)),
                ('fb_Sweeper_OPA_90', models.FloatField(blank=True, default=0)),
                ('fb_Sweeper_AvgDist', models.FloatField(blank=True, default=0)),
                ('created_data', models.DateTimeField(auto_now=True)),
                ('scrape_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapes.scrapejob')),
            ],
            options={
                'verbose_name': 'Datos de portero de FBRef',
                'verbose_name_plural': 'Datos de porteros de FBRef',
            },
        ),
        migrations.CreateModel(
            name='PlayerFbref',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fb_player_id', models.CharField(max_length=20)),
                ('fb_player_name', models.CharField(max_length=120)),
                ('fb_season', models.CharField(max_length=30)),
                ('fb_nation', models.CharField(max_length=3)),
                ('fb_pos', models.CharField(max_length=10, verbose_name='fb_position')),
                ('fb_team', models.CharField(blank=True, max_length=50)),
                ('fb_comp', models.CharField(max_length=50, verbose_name='fb_competition')),
                ('fb_born', models.CharField(blank=True, max_length=4)),
                ('fb_playing_time_MP', models.IntegerField(blank=True, default=0)),
                ('fb_playing_time_starts', models.IntegerField(blank=True, default=0)),
                ('fb_playing_time_min', models.IntegerField(blank=True, default=0)),
                ('fb_playing_time_90s', models.FloatField(blank=True, default=0)),
                ('fb_Gls', models.IntegerField(blank=True, default=0)),
                ('fb_Ast', models.IntegerField(blank=True, default=0)),
                ('fb_G_minus_PK', models.IntegerField(blank=True, default=0)),
                ('fb_PK', models.IntegerField(blank=True, default=0)),
                ('fb_PKatt', models.IntegerField(blank=True, default=0)),
                ('fb_CrdY', models.IntegerField(blank=True, default=0)),
                ('fb_CrdR', models.IntegerField(blank=True, default=0)),
                ('fb_Gls_90', models.FloatField(blank=True, default=0)),
                ('fb_Ast_90', models.FloatField(blank=True, default=0)),
                ('fb_G_plus_A_90', models.FloatField(blank=True, default=0)),
                ('fb_G_plus_A_minus_PK', models.FloatField(blank=True, default=0)),
                ('fb_xG', models.FloatField(blank=True, default=0)),
                ('fb_npxG', models.FloatField(blank=True, default=0)),
                ('fb_xA', models.FloatField(blank=True, default=0)),
                ('fb_npxG_plus_xA', models.FloatField(blank=True, default=0)),
                ('fb_xG_90', models.FloatField(blank=True, default=0)),
                ('fb_xA_90', models.FloatField(blank=True, default=0)),
                ('fb_xG_plus_xA_90', models.FloatField(blank=True, default=0)),
                ('fb_npxG_90', models.FloatField(blank=True, default=0)),
                ('fb_npxG_plus_xA_90', models.FloatField(blank=True, default=0)),
                ('fb_Sh', models.IntegerField(blank=True, default=0)),
                ('fb_SoT', models.IntegerField(blank=True, default=0)),
                ('fb_SoT_perc', models.FloatField(blank=True, default=0)),
                ('fb_Sh_90', models.FloatField(blank=True, default=0)),
                ('fb_SoT_90', models.FloatField(blank=True, default=0)),
                ('fb_G_vs_Sh', models.FloatField(blank=True, default=0)),
                ('fb_G_vs_SoT', models.FloatField(blank=True, default=0)),
                ('fb_Dist', models.FloatField(blank=True, default=0)),
                ('fb_FK', models.IntegerField(blank=True, default=0)),
                ('fb_npxG_vs_Sh', models.FloatField(blank=True, default=0)),
                ('fb_G_minus_xG', models.FloatField(blank=True, default=0)),
                ('fb_npxG_minus_xG', models.FloatField(blank=True, default=0)),
                ('fb_passes_Cmp', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Att', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Cmp_perc', models.FloatField(blank=True, default=0)),
                ('fb_passes_TotDist', models.IntegerField(blank=True, default=0)),
                ('fb_passes_PrgDist', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Short_Cmp', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Short_Att', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Short_Cmp_perc', models.FloatField(blank=True, default=0)),
                ('fb_passes_Medium_Cmp', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Medium_Att', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Medium_Cmp_perc', models.FloatField(blank=True, default=0)),
                ('fb_passes_Long_Cmp', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Long_Att', models.IntegerField(blank=True, default=0)),
                ('fb_passes_Long_Cmp_perc', models.FloatField(blank=True, default=0)),
                ('fb_A_minus_xA', models.FloatField(blank=True, default=0)),
                ('fb_key_passes', models.IntegerField(blank=True, default=0)),
                ('fb_last_third_passes', models.IntegerField(blank=True, default=0)),
                ('fb_PPA', models.IntegerField(blank=True, default=0)),
                ('fb_CrsPA', models.IntegerField(blank=True, default=0)),
                ('fb_progresive_passes', models.IntegerField(blank=True, default=0)),
                ('fb_progresive_passes_Att', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_Live', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_Dead', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_FK', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_TB', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_Press', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_Sw', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_Crs', models.IntegerField(blank=True, default=0)),
                ('fb_Pass_Types_CK', models.IntegerField(blank=True, default=0)),
                ('fb_Corner_Kicks_In', models.IntegerField(blank=True, default=0)),
                ('fb_Corner_Kicks_Out', models.IntegerField(blank=True, default=0)),
                ('fb_Corner_Kicks_Str', models.IntegerField(blank=True, default=0)),
                ('fb_Height_Ground', models.IntegerField(blank=True, default=0)),
                ('fb_Height_Low', models.IntegerField(blank=True, default=0)),
                ('fb_Height_High', models.IntegerField(blank=True, default=0)),
                ('fb_Body_Parts_Left', models.IntegerField(blank=True, default=0)),
                ('fb_Body_Parts_Right', models.IntegerField(blank=True, default=0)),
                ('fb_Body_Parts_Head', models.IntegerField(blank=True, default=0)),
                ('fb_Body_Parts_TI', models.IntegerField(blank=True, default=0)),
                ('fb_Body_Parts_Other', models.IntegerField(blank=True, default=0)),
                ('fb_Outcomes_Cmp', models.IntegerField(blank=True, default=0)),
                ('fb_Outcomes_Offsides', models.IntegerField(blank=True, default=0)),
                ('fb_Outcomes_Out', models.IntegerField(blank=True, default=0)),
                ('fb_Outcomes_Int', models.IntegerField(blank=True, default=0)),
                ('fb_Outcomes_Blocks', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_SCA', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_SCA90', models.FloatField(blank=True, default=0)),
                ('fb_SCA_Types_PassLive', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_Types_PassDead', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_Types_Drib', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_Types_Sh', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_Types_Fld', models.IntegerField(blank=True, default=0)),
                ('fb_SCA_Types_Def', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_GCA', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_GCA90', models.FloatField(blank=True, default=0)),
                ('fb_GCA_Types_PassLive', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_Types_PassDead', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_Types_Drib', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_Types_Sh', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_Types_Fld', models.IntegerField(blank=True, default=0)),
                ('fb_GCA_Types_Def', models.IntegerField(blank=True, default=0)),
                ('fb_Tackles_Tkl', models.IntegerField(blank=True, default=0)),
                ('fb_Tackles_TklW', models.IntegerField(blank=True, default=0)),
                ('fb_Tackles_Def_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Tackles_Mid_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Tackles_Att_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_vs_Dribbles_Tkl', models.IntegerField(blank=True, default=0)),
                ('fb_vs_Dribbles_Att', models.IntegerField(blank=True, default=0)),
                ('fb_vs_Dribbles_Tkl_perc', models.FloatField(blank=True, default=0)),
                ('fb_vs_Dribbles_Past', models.IntegerField(blank=True, default=0)),
                ('fb_Pressures_Press', models.IntegerField(blank=True, default=0)),
                ('fb_Pressures_Succ', models.IntegerField(blank=True, default=0)),
                ('fb_Pressures_perc', models.FloatField(blank=True, default=0)),
                ('fb_Pressures_Def_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Pressures_Mid_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Pressures_Att_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Blocks', models.IntegerField(blank=True, default=0)),
                ('fb_Blocks_Sh', models.IntegerField(blank=True, default=0)),
                ('fb_Blocks_ShSv', models.IntegerField(blank=True, default=0)),
                ('fb_Blocks_Pass', models.IntegerField(blank=True, default=0)),
                ('fb_Interceptions', models.IntegerField(blank=True, default=0)),
                ('fb_Tkl_plus_Int', models.IntegerField(blank=True, default=0)),
                ('fb_Clearances', models.IntegerField(blank=True, default=0)),
                ('fb_Errors', models.IntegerField(blank=True, default=0)),
                ('fb_Touches', models.IntegerField(blank=True, default=0)),
                ('fb_Touches_Def_Pen', models.IntegerField(blank=True, default=0)),
                ('fb_Touches_Def_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Touches_Mid_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Touches_Att_3rd', models.IntegerField(blank=True, default=0)),
                ('fb_Touches_Att_Pen', models.IntegerField(blank=True, default=0)),
                ('fb_Touches_Live', models.IntegerField(blank=True, default=0)),
                ('fb_Dribbles_Succ', models.IntegerField(blank=True, default=0)),
                ('fb_Dribbles_Att', models.IntegerField(blank=True, default=0)),
                ('fb_Dribbles_Succ_perc', models.FloatField(blank=True, default=0)),
                ('fb_Dribbles_number_Pl', models.IntegerField(blank=True, default=0)),
                ('fb_Dribbles_Megs', models.IntegerField(blank=True, default=0)),
                ('fb_Carries', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_TotDist', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_PrgDist', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_Prog', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_last_third', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_CPA', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_Mis', models.IntegerField(blank=True, default=0)),
                ('fb_Carries_Dis', models.IntegerField(blank=True, default=0)),
                ('fb_Receiving_Targ', models.IntegerField(blank=True, default=0)),
                ('fb_Receiving_Rec', models.IntegerField(blank=True, default=0)),
                ('fb_Receiving_Rec_perc', models.FloatField(blank=True, default=0)),
                ('fb_Receiving_Prog', models.IntegerField(blank=True, default=0)),
                ('fb_Playing_Time_Mn_vs_MP', models.IntegerField(blank=True, default=0)),
                ('fb_Playing_Time_Min_perc', models.FloatField(blank=True, default=0)),
                ('fb_Starts_Min_vs_Start', models.IntegerField(blank=True, default=0)),
                ('fb_Starts_Compl', models.IntegerField(blank=True, default=0)),
                ('fb_Subs_Subs', models.IntegerField(blank=True, default=0)),
                ('fb_Subs_Mn_vs_Sub', models.IntegerField(blank=True, default=0)),
                ('fb_Subs_unSub', models.IntegerField(blank=True, default=0)),
                ('fb_Team_Success_PPM', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_onG', models.IntegerField(blank=True, default=0)),
                ('fb_Team_Success_onGA', models.IntegerField(blank=True, default=0)),
                ('fb_Team_Success_dif', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_dif_90', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_On_Off', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_xG_onxG', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_xG_onxGA', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_xG_xGdif', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_xG_xGdif_90', models.FloatField(blank=True, default=0)),
                ('fb_Team_Success_xG_On_Off', models.FloatField(blank=True, default=0)),
                ('fb_Performance_2CrdY', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_Fouls', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_Fouls_drawn', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_Offsides', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_Cross', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_Interceptions', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_TklW', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_PKwon', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_PKconceded', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_OG', models.IntegerField(blank=True, default=0)),
                ('fb_Performance_Recov', models.IntegerField(blank=True, default=0)),
                ('fb_Aerial_Duels_Won', models.IntegerField(blank=True, default=0)),
                ('fb_Aerial_Duels_Lost', models.IntegerField(blank=True, default=0)),
                ('fb_Aerial_Duels_Won_perc', models.FloatField(blank=True, default=0)),
                ('created_data', models.DateTimeField(auto_now=True)),
                ('scrape_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapes.scrapejob')),
            ],
            options={
                'verbose_name': 'Datos de jugador de FBRef',
                'verbose_name_plural': 'Datos de jugadores de FBRef',
            },
        ),
        migrations.CreateModel(
            name='PlayerCapology',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ca_player_id', models.CharField(max_length=150)),
                ('ca_player_name', models.CharField(max_length=120)),
                ('ca_salary', models.DecimalField(decimal_places=2, max_digits=12)),
                ('ca_expiration', models.DateField(blank=True)),
                ('ca_country', models.CharField(max_length=100)),
                ('ca_team', models.CharField(max_length=100)),
                ('ca_season', models.CharField(max_length=30)),
                ('ca_comp', models.CharField(max_length=50)),
                ('created_data', models.DateTimeField(auto_now=True)),
                ('scrape_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrapes.scrapejob')),
            ],
            options={
                'verbose_name': 'Datos de jugador de Capology',
                'verbose_name_plural': 'Datos de jugadores de Capology',
            },
        ),
        migrations.AddConstraint(
            model_name='playerunderstat',
            constraint=models.UniqueConstraint(fields=('us_player_id', 'us_season', 'us_team'), name='unique_player_id_season_team_combination_us'),
        ),
        migrations.AddConstraint(
            model_name='playerfbrefgk',
            constraint=models.UniqueConstraint(fields=('fb_player_id', 'fb_season', 'fb_team'), name='unique_player_id_season_team_combination_fbref_gk'),
        ),
        migrations.AddConstraint(
            model_name='playerfbref',
            constraint=models.UniqueConstraint(fields=('fb_player_id', 'fb_season', 'fb_team'), name='unique_player_id_season_team_combination_fbref_players'),
        ),
    ]
