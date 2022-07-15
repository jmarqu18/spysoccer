from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Max

# Base
import pandas as pd
import numpy as np


from scrapes.models import (
    PlayerFbref,
    ScrapeJob,
    PlayerCapology,
    PlayerFbrefGK,
    PlayerTransfermarkt,
    PlayerUnderstat,
)
from players.models import Player, PlayerStats, GoalkeeperStats


class Command(BaseCommand):
    help = "Comprueba si los datos extraidos son los más actuales y los copia en la BBDD si no."
    # define logic of command

    # def add_arguments(self, parser):
    #     parser.add_argument("season", type=str)

    def handle(self, *args, **options):
        # Definimos las variables para crear la línea de scrape_job

        # Traemos los datos de Player como "mapeo"
        queryset = Player.objects.values_list(
            "id", "id_fbref", "id_understat", "id_transfermarkt", "id_capology"
        )
        players_mapping = pd.DataFrame(
            list(queryset),
            columns=[
                "id",
                "id_fbref",
                "id_understat",
                "id_transfermarkt",
                "id_capology",
            ],
        )

        # players_mapping.to_csv("./data_export/players_mapping.csv", index=False)

        queryset2 = PlayerFbref.objects.values_list()
        qs_cols = PlayerFbref._meta.get_fields()
        data_fbref = pd.DataFrame(list(queryset2), columns=qs_cols)

        # data_fbref.to_csv("./data_export/data_fbref.csv", index=False)

        queryset2 = PlayerFbrefGK.objects.values_list()
        qs_cols = PlayerFbrefGK._meta.get_fields()
        data_fbref_gk = pd.DataFrame(list(queryset2), columns=qs_cols)

        # data_fbref_gk.to_csv("./data_export/data_fbref_gk.csv", index=False)

        queryset2 = PlayerCapology.objects.values_list()
        qs_cols = PlayerCapology._meta.get_fields()
        data_capology = pd.DataFrame(list(queryset2), columns=qs_cols)

        # data_capology.to_csv("./data_export/data_capology.csv", index=False)

        queryset2 = PlayerUnderstat.objects.values_list()
        qs_cols = PlayerUnderstat._meta.get_fields()
        data_understat = pd.DataFrame(list(queryset2), columns=qs_cols)

        # data_understat.to_csv("./data_export/data_understat.csv", index=False)

        queryset2 = PlayerTransfermarkt.objects.values_list()
        qs_cols = PlayerTransfermarkt._meta.get_fields()
        data_tm = pd.DataFrame(list(queryset2), columns=qs_cols)

        # data_tm.to_csv("./data_export/data_tm.csv", index=False)

        # Limpiamos los nombres de las columnas
        models = {
            "PlayerCapology": data_capology,
            "PlayerUnderstat": data_understat,
            "PlayerTransfermarkt": data_tm,
            "PlayerFbref": data_fbref,
            "PlayerFbrefGK": data_fbref_gk,
        }

        dfs_names = [
            "data_capology",
            "data_understat",
            "data_tm",
            "data_fbref",
            "data_fbref_gk",
        ]

        for i, key in enumerate(models):
            cols = []
            replace_text = "scrapes.{}.".format(key)
            for col in models[key].columns:
                cols.append(str(col).replace(replace_text, ""))
            locals()[dfs_names[i]].columns = cols

        # Cambiamos los tipos de datos para coincidir con el destino (players_mapping)
        data_understat["us_player_id"] = data_understat["us_player_id"].astype(str)
        data_tm["tm_player_id"] = data_tm["tm_player_id"].astype(str)

        # Definimos las columnas necesarias de cada dataframe
        cols_tm = [
            "tm_player_id",
            "tm_date_joined",
            "tm_contract_expires",
            "tm_current_value",
        ]
        cols_ca = ["ca_player_id", "ca_salary"]
        cols_us = [
            "us_player_id",
            "us_xGChain",
            "us_xGBuildup",
            "us_xGChain_90",
            "us_xGBuildup_90",
        ]
        cols_fb = [
            "fb_player_id",
            "fb_season",
            "fb_team",
            "fb_comp",
            "fb_playing_time_MP",
            "fb_playing_time_starts",
            "fb_playing_time_min",
            "fb_Playing_Time_Mn_vs_MP",
            "fb_Playing_Time_Min_perc",
            "fb_Starts_Compl",
            "fb_Subs_Subs",
            "fb_Starts_Min_vs_Start",
            "fb_Subs_Mn_vs_Sub",
            "fb_playing_time_90s",
            "fb_Gls",
            "fb_Ast",
            "fb_G_minus_PK",
            "fb_PK",
            "fb_PKatt",
            "fb_G_plus_A_minus_PK",
            "fb_xG",
            "fb_npxG",
            "fb_xA",
            "fb_npxG_plus_xA",
            "fb_Gls_90",
            "fb_Ast_90",
            "fb_G_plus_A_90",
            "fb_xG_90",
            "fb_xA_90",
            "fb_npxG_90",
            "fb_npxG_plus_xA_90",
            "fb_A_minus_xA",
            "fb_Sh",
            "fb_SoT",
            "fb_SoT_perc",
            "fb_Sh_90",
            "fb_SoT_90",
            "fb_G_vs_Sh",
            "fb_G_vs_SoT",
            "fb_Dist",
            "fb_FK",
            "fb_npxG_vs_Sh",
            "fb_G_minus_xG",
            "fb_passes_Cmp",
            "fb_passes_Att",
            "fb_passes_Cmp_perc",
            "fb_passes_TotDist",
            "fb_passes_PrgDist",
            "fb_passes_Short_Cmp",
            "fb_passes_Short_Att",
            "fb_passes_Short_Cmp_perc",
            "fb_passes_Medium_Cmp",
            "fb_passes_Medium_Att",
            "fb_passes_Medium_Cmp_perc",
            "fb_passes_Long_Cmp",
            "fb_passes_Long_Att",
            "fb_passes_Long_Cmp_perc",
            "fb_key_passes",
            "fb_last_third_passes",
            "fb_PPA",
            "fb_CrsPA",
            "fb_progresive_passes",
            "fb_progresive_passes_Att",
            "fb_Pass_Types_Live",
            "fb_Pass_Types_Dead",
            "fb_Pass_Types_FK",
            "fb_Pass_Types_TB",
            "fb_Pass_Types_Press",
            "fb_Pass_Types_Sw",
            "fb_Pass_Types_Crs",
            "fb_Pass_Types_CK",
            "fb_Corner_Kicks_In",
            "fb_Corner_Kicks_Out",
            "fb_Corner_Kicks_Str",
            "fb_Height_Ground",
            "fb_Height_Low",
            "fb_Height_High",
            "fb_Body_Parts_Left",
            "fb_Body_Parts_Right",
            "fb_Body_Parts_Head",
            "fb_Body_Parts_TI",
            "fb_Body_Parts_Other",
            "fb_Outcomes_Offsides",
            "fb_Outcomes_Out",
            "fb_Outcomes_Int",
            "fb_Outcomes_Blocks",
            "fb_SCA_SCA",
            "fb_SCA_SCA90",
            "fb_SCA_Types_PassLive",
            "fb_SCA_Types_PassDead",
            "fb_SCA_Types_Drib",
            "fb_SCA_Types_Sh",
            "fb_SCA_Types_Fld",
            "fb_SCA_Types_Def",
            "fb_GCA_GCA",
            "fb_GCA_GCA90",
            "fb_GCA_Types_PassLive",
            "fb_GCA_Types_PassDead",
            "fb_GCA_Types_Drib",
            "fb_GCA_Types_Sh",
            "fb_GCA_Types_Fld",
            "fb_GCA_Types_Def",
            "fb_Tackles_Tkl",
            "fb_Tackles_TklW",
            "fb_Tackles_Def_3rd",
            "fb_Tackles_Mid_3rd",
            "fb_Tackles_Att_3rd",
            "fb_vs_Dribbles_Tkl",
            "fb_vs_Dribbles_Att",
            "fb_vs_Dribbles_Tkl_perc",
            "fb_Pressures_Press",
            "fb_Pressures_Succ",
            "fb_Pressures_perc",
            "fb_Pressures_Def_3rd",
            "fb_Pressures_Mid_3rd",
            "fb_Pressures_Att_3rd",
            "fb_Blocks",
            "fb_Blocks_Sh",
            "fb_Blocks_ShSv",
            "fb_Blocks_Pass",
            "fb_Interceptions",
            "fb_Tkl_plus_Int",
            "fb_Clearances",
            "fb_Errors",
            "fb_Aerial_Duels_Won",
            "fb_Aerial_Duels_Lost",
            "fb_Aerial_Duels_Won_perc",
            "fb_Touches",
            "fb_Touches_Def_Pen",
            "fb_Touches_Def_3rd",
            "fb_Touches_Mid_3rd",
            "fb_Touches_Att_3rd",
            "fb_Touches_Att_Pen",
            "fb_Dribbles_Succ",
            "fb_Dribbles_Att",
            "fb_Dribbles_Succ_perc",
            "fb_Dribbles_number_Pl",
            "fb_Dribbles_Megs",
            "fb_Carries",
            "fb_Carries_TotDist",
            "fb_Carries_PrgDist",
            "fb_Carries_Prog",
            "fb_Carries_last_third",
            "fb_Carries_CPA",
            "fb_Carries_Mis",
            "fb_Carries_Dis",
            "fb_Receiving_Targ",
            "fb_Receiving_Rec",
            "fb_Receiving_Rec_perc",
            "fb_Receiving_Prog",
            "fb_CrdY",
            "fb_CrdR",
            "fb_Performance_2CrdY",
            "fb_Performance_Fouls",
            "fb_Performance_Fouls_drawn",
            "fb_Performance_Offsides",
            "fb_Performance_PKwon",
            "fb_Performance_PKconceded",
            "fb_Performance_OG",
            "fb_Performance_Recov",
        ]
        cols_fb_gk = [
            "fb_player_id",
            "fb_season",
            "fb_team",
            "fb_comp",
            "fb_playing_time_MP",
            "fb_playing_time_starts",
            "fb_playing_time_min",
            "fb_playing_time_90s",
            "fb_Ast",
            "fb_xA",
            "fb_Ast_90",
            "fb_xA_90",
            "fb_GA",
            "fb_GA_90",
            "fb_SoTA",
            "fb_saves",
            "fb_save_perc",
            "fb_CS",
            "fb_CS_perc",
            "fb_PK_against",
            "fb_PK_saves",
            "fb_PK_saves_perc",
            "fb_PSxG",
            "fb_PSxG_vs_SoT",
            "fb_PSxG_dif",
            "fb_Launched_Cmp",
            "fb_Launched_Att",
            "fb_Launched_Cmp_perc",
            "fb_Passes_Att",
            "fb_Passes_AvgLen",
            "fb_Goal_Kicks_Att",
            "fb_Goal_Kicks_Launch_perc",
            "fb_Goal_Kicks_AvgLen",
            "fb_Crosses_Opp",
            "fb_Crosses_Stp",
            "fb_Crosses_Stp_perc",
            "fb_Sweeper_OPA",
            "fb_Sweeper_OPA_90",
            "fb_Sweeper_AvgDist",
            "fb_CrdY",
            "fb_CrdR",
        ]

        # Comenzamos a mergear con lso dataframes de destino
        df_base = players_mapping.merge(
            data_capology[cols_ca],
            left_on="id_capology",
            right_on="ca_player_id",
            how="left",
        ).drop(columns="ca_player_id")

        df_base = df_base.merge(
            data_tm[cols_tm],
            left_on="id_transfermarkt",
            right_on="tm_player_id",
            how="left",
        ).drop(columns="tm_player_id")

        df_base.reset_index(drop=True, inplace=True)

        # Con esta base ahora separamos porteros y jugadores
        # Jugadores
        df_playerstats = df_base.merge(
            data_understat[cols_us],
            how="left",
            left_on="id_understat",
            right_on="us_player_id",
        ).drop(columns="us_player_id")

        df_playerstats = (
            df_playerstats.merge(
                data_fbref[cols_fb],
                how="left",
                left_on="id_fbref",
                right_on="fb_player_id",
            )
            .drop(columns="fb_player_id")
            .drop_duplicates(["id", "fb_season", "fb_team"])
        )

        # Quitamos a los porteros
        df_playerstats = df_playerstats.loc[~df_playerstats["fb_season"].isna()]

        # Porteros
        df_goalkeeperstats = (
            df_base.merge(
                data_fbref_gk[cols_fb_gk],
                how="left",
                left_on="id_fbref",
                right_on="fb_player_id",
            )
            .drop(columns="fb_player_id")
            .drop_duplicates(["id", "fb_season", "fb_team"])
        )

        # Quitamos a los jugadores
        df_goalkeeperstats = df_goalkeeperstats.loc[
            ~df_goalkeeperstats["fb_season"].isna()
        ]

        # Ultimas limpiezas de datos necesarias para guardar
        df_goalkeeperstats["ca_salary"] = np.where(
            df_goalkeeperstats["ca_salary"].isnull(), 0, df_goalkeeperstats["ca_salary"]
        )
        df_playerstats["ca_salary"] = np.where(
            df_playerstats["ca_salary"].isnull(), 0, df_playerstats["ca_salary"]
        )
        df_goalkeeperstats["tm_current_value"] = np.where(
            df_goalkeeperstats["tm_current_value"].isnull(),
            0,
            df_goalkeeperstats["tm_current_value"],
        )
        df_playerstats["tm_current_value"] = np.where(
            df_playerstats["tm_current_value"].isnull(),
            0,
            df_playerstats["tm_current_value"],
        )

        df_playerstats["tm_date_joined"] = df_playerstats["tm_date_joined"].apply(
            lambda x: x
            if not pd.isnull(x)
            else datetime.strptime("1900-01-01", "%Y-%m-%d")
        )
        df_playerstats["tm_contract_expires"] = df_playerstats[
            "tm_contract_expires"
        ].apply(
            lambda x: x
            if not pd.isnull(x)
            else datetime.strptime("1900-01-01", "%Y-%m-%d")
        )
        df_goalkeeperstats["tm_date_joined"] = df_goalkeeperstats[
            "tm_date_joined"
        ].apply(
            lambda x: x
            if not pd.isnull(x)
            else datetime.strptime("1900-01-01", "%Y-%m-%d")
        )
        df_goalkeeperstats["tm_contract_expires"] = df_goalkeeperstats[
            "tm_contract_expires"
        ].apply(
            lambda x: x
            if not pd.isnull(x)
            else datetime.strptime("1900-01-01", "%Y-%m-%d")
        )

        # TODO: Evitar que se suban registros duplicados comparando lo que ya tenemos
        # con lo nuevo

        # Vamos a Insertar los datos en la BBDD
        scrape_job = ScrapeJob.objects.latest("completed_date")
        scrape_date = scrape_job.completed_date

        players_stats = [
            PlayerStats(
                player=Player.objects.get(id=row["id"]),
                extraction_date=scrape_date,
                season=row["fb_season"],
                team=row["fb_team"],
                team_date_joined=row["tm_date_joined"],
                team_contract_expires=row["tm_contract_expires"],
                competition=row["fb_comp"],
                salary=row["ca_salary"],
                current_value=row["tm_current_value"],
                matches_played=row["fb_playing_time_MP"],
                matches_starts=row["fb_playing_time_starts"],
                minutes_played=row["fb_playing_time_min"],
                minutes_per_match=row["fb_Playing_Time_Mn_vs_MP"],
                perc_minutes_played=row["fb_Playing_Time_Min_perc"],
                complete_matches_played=row["fb_Starts_Compl"],
                matches_as_substitute=row["fb_Subs_Subs"],
                mean_minutes_starts=row["fb_Starts_Min_vs_Start"],
                mean_minutes_substitute=row["fb_Subs_Mn_vs_Sub"],
                playing_time_90s=row["fb_playing_time_90s"],
                goals=row["fb_Gls"],
                assists=row["fb_Ast"],
                non_penalty_goals=row["fb_G_minus_PK"],
                penalty_goals=row["fb_PK"],
                penalty_shoots=row["fb_PKatt"],
                goals_plus_assists_minus_pk=row["fb_G_plus_A_minus_PK"],
                expected_goals=row["fb_xG"],
                npxg=row["fb_npxG"],
                expected_assists=row["fb_xA"],
                npxg_plus_expected_assists=row["fb_npxG_plus_xA"],
                goals_90=row["fb_Gls_90"],
                assists_90=row["fb_Ast_90"],
                goals_plus_assists_90=row["fb_G_plus_A_90"],
                expected_goals_90=row["fb_xG_90"],
                expected_assists_90=row["fb_xA_90"],
                npxg_90=row["fb_npxG_90"],
                npxg_plus_expected_assists_90=row["fb_npxG_plus_xA_90"],
                assists_minus_xA=row["fb_A_minus_xA"],
                shoots=row["fb_Sh"],
                shoots_on_target=row["fb_SoT"],
                perc_shoots_on_target=row["fb_SoT_perc"],
                shoots_90=row["fb_Sh_90"],
                shoots_on_target_90=row["fb_SoT_90"],
                goals_per_shoot=row["fb_G_vs_Sh"],
                goals_per_shoot_on_target=row["fb_G_vs_SoT"],
                mean_distance_from_goals_shoots=row["fb_Dist"],
                free_kicks_shooted=row["fb_FK"],
                npxg_per_shoot=row["fb_npxG_vs_Sh"],
                goals_minus_expected_goals=row["fb_G_minus_xG"],
                passes_completed=row["fb_passes_Cmp"],
                passes_attempted=row["fb_passes_Att"],
                perc_passes=row["fb_passes_Cmp_perc"],
                total_distance_passes=row["fb_passes_TotDist"],
                total_distance_progressive_passes=row["fb_passes_PrgDist"],
                short_passes_completed=row["fb_passes_Short_Cmp"],
                short_passes_attempted=row["fb_passes_Short_Att"],
                perc_short_passes=row["fb_passes_Short_Cmp_perc"],
                medium_passes_completed=row["fb_passes_Medium_Cmp"],
                medium_passes_attempted=row["fb_passes_Medium_Att"],
                perc_medium_passes=row["fb_passes_Medium_Cmp_perc"],
                long_passes_completed=row["fb_passes_Long_Cmp"],
                long_passes_attempted=row["fb_passes_Long_Att"],
                perc_long_passes=row["fb_passes_Long_Cmp_perc"],
                key_passes=row["fb_key_passes"],
                xGChain=row["us_xGChain"],
                xGBuildup=row["us_xGBuildup"],
                xGChain_90=row["us_xGChain_90"],
                xGBuildup_90=row["us_xGBuildup_90"],
                last_third_passes=row["fb_last_third_passes"],
                ppa=row["fb_PPA"],
                crosses_pa=row["fb_CrsPA"],
                progresive_passes=row["fb_progresive_passes"],
                progresive_passes_attempted=row["fb_progresive_passes_Att"],
                live_passes=row["fb_Pass_Types_Live"],
                dead_passes=row["fb_Pass_Types_Dead"],
                free_kick_passes=row["fb_Pass_Types_FK"],
                to_back_passes=row["fb_Pass_Types_TB"],
                pressed_passes=row["fb_Pass_Types_Press"],
                swap_passes=row["fb_Pass_Types_Sw"],
                crosses=row["fb_Pass_Types_Crs"],
                corner_kicks=row["fb_Pass_Types_CK"],
                corner_kicks_in=row["fb_Corner_Kicks_In"],
                corner_kicks_out=row["fb_Corner_Kicks_Out"],
                corner_kicks_straight=row["fb_Corner_Kicks_Str"],
                ground_passes=row["fb_Height_Ground"],
                low_passes=row["fb_Height_Low"],
                high_passes=row["fb_Height_High"],
                left_foot_passes=row["fb_Body_Parts_Left"],
                right_foot_passes=row["fb_Body_Parts_Right"],
                head_passes=row["fb_Body_Parts_Head"],
                throw_in_passes=row["fb_Body_Parts_TI"],
                other_body_parts_passes=row["fb_Body_Parts_Other"],
                offsides_passes=row["fb_Outcomes_Offsides"],
                out_off_bound_passes=row["fb_Outcomes_Out"],
                intercepted_passes=row["fb_Outcomes_Int"],
                blocked_passes=row["fb_Outcomes_Blocks"],
                sca=row["fb_SCA_SCA"],
                sca_90=row["fb_SCA_SCA90"],
                sca_live_pass=row["fb_SCA_Types_PassLive"],
                sca_dead_pass=row["fb_SCA_Types_PassDead"],
                sca_dribbling=row["fb_SCA_Types_Drib"],
                sca_another_shoot=row["fb_SCA_Types_Sh"],
                sca_foul_drawn=row["fb_SCA_Types_Fld"],
                sca_defensive_action=row["fb_SCA_Types_Def"],
                gca=row["fb_GCA_GCA"],
                gca_90=row["fb_GCA_GCA90"],
                gca_live_pass=row["fb_GCA_Types_PassLive"],
                gca_dead_pass=row["fb_GCA_Types_PassDead"],
                gca_dribbling=row["fb_GCA_Types_Drib"],
                gca_another_shoot=row["fb_GCA_Types_Sh"],
                gca_foul_drawn=row["fb_GCA_Types_Fld"],
                gca_defensive_action=row["fb_GCA_Types_Def"],
                tackles=row["fb_Tackles_Tkl"],
                tackles_wins=row["fb_Tackles_TklW"],
                tackles_def_third=row["fb_Tackles_Def_3rd"],
                tackles_mid_third=row["fb_Tackles_Mid_3rd"],
                tackles_att_third=row["fb_Tackles_Att_3rd"],
                tackles_vs_dribbles_wins=row["fb_vs_Dribbles_Tkl"],
                tackles_vs_dribbles_attempted=row["fb_vs_Dribbles_Att"],
                perc_tackles_vs_dribbles=row["fb_vs_Dribbles_Tkl_perc"],
                pressures=row["fb_Pressures_Press"],
                pressures_success=row["fb_Pressures_Succ"],
                perc_pressures_success=row["fb_Pressures_perc"],
                pressures_def_third=row["fb_Pressures_Def_3rd"],
                pressures_mid_third=row["fb_Pressures_Mid_3rd"],
                pressures_att_third=row["fb_Pressures_Att_3rd"],
                blocks=row["fb_Blocks"],
                blocks_shoots=row["fb_Blocks_Sh"],
                blocks_shoots_on_target=row["fb_Blocks_ShSv"],
                blocks_passes=row["fb_Blocks_Pass"],
                interceptions=row["fb_Interceptions"],
                tackles_plus_interceptions=row["fb_Tkl_plus_Int"],
                clearances=row["fb_Clearances"],
                errors_to_rival_shoot=row["fb_Errors"],
                aerial_duels_won=row["fb_Aerial_Duels_Won"],
                aerial_duels_lost=row["fb_Aerial_Duels_Lost"],
                perc_aerial_duels_won=row["fb_Aerial_Duels_Won_perc"],
                touches=row["fb_Touches"],
                touches_def_box=row["fb_Touches_Def_Pen"],
                touches_def_third=row["fb_Touches_Def_3rd"],
                touches_mid_third=row["fb_Touches_Mid_3rd"],
                touches_att_third=row["fb_Touches_Att_3rd"],
                touches_att_box=row["fb_Touches_Att_Pen"],
                dribbles_success=row["fb_Dribbles_Succ"],
                dribbles_attempted=row["fb_Dribbles_Att"],
                perc_dribbles_success=row["fb_Dribbles_Succ_perc"],
                number_players_dribbled=row["fb_Dribbles_number_Pl"],
                dribbles_megs=row["fb_Dribbles_Megs"],
                carries=row["fb_Carries"],
                distance_carries=row["fb_Carries_TotDist"],
                progressive_distance_carries=row["fb_Carries_PrgDist"],
                progressive_carries=row["fb_Carries_Prog"],
                carries_last_third=row["fb_Carries_last_third"],
                carries_to_att_box=row["fb_Carries_CPA"],
                carries_missed=row["fb_Carries_Mis"],
                carries_intercepted=row["fb_Carries_Dis"],
                receiving_target=row["fb_Receiving_Targ"],
                receiving_target_success=row["fb_Receiving_Rec"],
                perc_receiving_target_success=row["fb_Receiving_Rec_perc"],
                receiving_target_progressive=row["fb_Receiving_Prog"],
                yellow_cards=row["fb_CrdY"],
                red_cards=row["fb_CrdR"],
                double_yellow_cards=row["fb_Performance_2CrdY"],
                fouls=row["fb_Performance_Fouls"],
                fouls_drawn=row["fb_Performance_Fouls_drawn"],
                offsides=row["fb_Performance_Offsides"],
                penalties_wons=row["fb_Performance_PKwon"],
                penalties_conceded=row["fb_Performance_PKconceded"],
                own_goals=row["fb_Performance_OG"],
                recoveries=row["fb_Performance_Recov"],
            )
            for i, row in df_playerstats.iterrows()
        ]

        if players_stats:
            PlayerStats.objects.bulk_create(players_stats, 1000)

        gk_stats = [
            GoalkeeperStats(
                player=Player.objects.get(id=row["id"]),
                extraction_date=scrape_date,
                season=row["fb_season"],
                team=row["fb_team"],
                team_date_joined=row["tm_date_joined"],
                team_contract_expires=row["tm_contract_expires"],
                competition=row["fb_comp"],
                salary=row["ca_salary"],
                current_value=row["tm_current_value"],
                matches_played=row["fb_playing_time_MP"],
                matches_starts=row["fb_playing_time_starts"],
                minutes_played=row["fb_playing_time_min"],
                playing_time_90s=row["fb_playing_time_90s"],
                assists=row["fb_Ast"],
                expected_assists=row["fb_xA"],
                assists_90=row["fb_Ast_90"],
                expected_assists_90=row["fb_xA_90"],
                goals_against=row["fb_GA"],
                goals_against_90=row["fb_GA_90"],
                shoots_on_target_against=row["fb_SoTA"],
                saves=row["fb_saves"],
                perc_saves=row["fb_save_perc"],
                clear_scores=row["fb_CS"],
                perc_clear_scores=row["fb_CS_perc"],
                penalty_against=row["fb_PK_against"],
                penalty_saves=row["fb_PK_saves"],
                perc_penalty_saves=row["fb_PK_saves_perc"],
                psxg=row["fb_PSxG"],
                psxg_per_shoots=row["fb_PSxG_vs_SoT"],
                psxg_diference=row["fb_PSxG_dif"],
                launches_completed=row["fb_Launched_Cmp"],
                launches_attempted=row["fb_Launched_Att"],
                perc_launches_completed=row["fb_Launched_Cmp_perc"],
                passes_attempted=row["fb_Passes_Att"],
                average_lenght_passes=row["fb_Passes_AvgLen"],
                goal_kicks_attempted=row["fb_Goal_Kicks_Att"],
                perc_goal_kicks_completed=row["fb_Goal_Kicks_Launch_perc"],
                average_lenght_goal_kick=row["fb_Goal_Kicks_AvgLen"],
                opponent_crosses=row["fb_Crosses_Opp"],
                opponent_crosses_stopped=row["fb_Crosses_Stp"],
                perc_opponent_crosses_stopped=row["fb_Crosses_Stp_perc"],
                sweeper_opa=row["fb_Sweeper_OPA"],
                sweeper_opa_90=row["fb_Sweeper_OPA_90"],
                average_distance_sweeper=row["fb_Sweeper_AvgDist"],
                yellow_cards=row["fb_CrdY"],
                red_cards=row["fb_CrdR"],
            )
            for i, row in df_goalkeeperstats.iterrows()
        ]

        if gk_stats:
            GoalkeeperStats.objects.bulk_create(gk_stats, 1000)
