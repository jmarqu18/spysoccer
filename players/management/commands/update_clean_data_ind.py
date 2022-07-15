from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Max

# Base
import pandas as pd
import numpy as np
from tqdm import tqdm
import traceback


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

        df_playerstats.reset_index(drop=True, inplace=True)
        df_goalkeeperstats.reset_index(drop=True, inplace=True)

        print("Guardando información de los jugadores en la base de datos")
        for i in tqdm(range(len(df_playerstats))):
            PlayerStats.objects.get_or_create(
                player=Player.objects.get(id=df_playerstats["id"][i]),
                extraction_date=scrape_date,
                season=df_playerstats["fb_season"][i],
                team=df_playerstats["fb_team"][i],
                team_date_joined=df_playerstats["tm_date_joined"][i],
                team_contract_expires=df_playerstats["tm_contract_expires"][i],
                competition=df_playerstats["fb_comp"][i],
                salary=df_playerstats["ca_salary"][i],
                current_value=df_playerstats["tm_current_value"][i],
                matches_played=df_playerstats["fb_playing_time_MP"][i],
                matches_starts=df_playerstats["fb_playing_time_starts"][i],
                minutes_played=df_playerstats["fb_playing_time_min"][i],
                minutes_per_match=df_playerstats["fb_Playing_Time_Mn_vs_MP"][i],
                perc_minutes_played=df_playerstats["fb_Playing_Time_Min_perc"][i],
                complete_matches_played=df_playerstats["fb_Starts_Compl"][i],
                matches_as_substitute=df_playerstats["fb_Subs_Subs"][i],
                mean_minutes_starts=df_playerstats["fb_Starts_Min_vs_Start"][i],
                mean_minutes_substitute=df_playerstats["fb_Subs_Mn_vs_Sub"][i],
                playing_time_90s=df_playerstats["fb_playing_time_90s"][i],
                goals=df_playerstats["fb_Gls"][i],
                assists=df_playerstats["fb_Ast"][i],
                non_penalty_goals=df_playerstats["fb_G_minus_PK"][i],
                penalty_goals=df_playerstats["fb_PK"][i],
                penalty_shoots=df_playerstats["fb_PKatt"][i],
                goals_plus_assists_minus_pk=df_playerstats["fb_G_plus_A_minus_PK"][i],
                expected_goals=df_playerstats["fb_xG"][i],
                npxg=df_playerstats["fb_npxG"][i],
                expected_assists=df_playerstats["fb_xA"][i],
                npxg_plus_expected_assists=df_playerstats["fb_npxG_plus_xA"][i],
                goals_90=df_playerstats["fb_Gls_90"][i],
                assists_90=df_playerstats["fb_Ast_90"][i],
                goals_plus_assists_90=df_playerstats["fb_G_plus_A_90"][i],
                expected_goals_90=df_playerstats["fb_xG_90"][i],
                expected_assists_90=df_playerstats["fb_xA_90"][i],
                npxg_90=df_playerstats["fb_npxG_90"][i],
                npxg_plus_expected_assists_90=df_playerstats["fb_npxG_plus_xA_90"][i],
                assists_minus_xA=df_playerstats["fb_A_minus_xA"][i],
                shoots=df_playerstats["fb_Sh"][i],
                shoots_on_target=df_playerstats["fb_SoT"][i],
                perc_shoots_on_target=df_playerstats["fb_SoT_perc"][i],
                shoots_90=df_playerstats["fb_Sh_90"][i],
                shoots_on_target_90=df_playerstats["fb_SoT_90"][i],
                goals_per_shoot=df_playerstats["fb_G_vs_Sh"][i],
                goals_per_shoot_on_target=df_playerstats["fb_G_vs_SoT"][i],
                mean_distance_from_goals_shoots=df_playerstats["fb_Dist"][i],
                free_kicks_shooted=df_playerstats["fb_FK"][i],
                npxg_per_shoot=df_playerstats["fb_npxG_vs_Sh"][i],
                goals_minus_expected_goals=df_playerstats["fb_G_minus_xG"][i],
                passes_completed=df_playerstats["fb_passes_Cmp"][i],
                passes_attempted=df_playerstats["fb_passes_Att"][i],
                perc_passes=df_playerstats["fb_passes_Cmp_perc"][i],
                total_distance_passes=df_playerstats["fb_passes_TotDist"][i],
                total_distance_progressive_passes=df_playerstats["fb_passes_PrgDist"][
                    i
                ],
                short_passes_completed=df_playerstats["fb_passes_Short_Cmp"][i],
                short_passes_attempted=df_playerstats["fb_passes_Short_Att"][i],
                perc_short_passes=df_playerstats["fb_passes_Short_Cmp_perc"][i],
                medium_passes_completed=df_playerstats["fb_passes_Medium_Cmp"][i],
                medium_passes_attempted=df_playerstats["fb_passes_Medium_Att"][i],
                perc_medium_passes=df_playerstats["fb_passes_Medium_Cmp_perc"][i],
                long_passes_completed=df_playerstats["fb_passes_Long_Cmp"][i],
                long_passes_attempted=df_playerstats["fb_passes_Long_Att"][i],
                perc_long_passes=df_playerstats["fb_passes_Long_Cmp_perc"][i],
                key_passes=df_playerstats["fb_key_passes"][i],
                xGChain=df_playerstats["us_xGChain"][i],
                xGBuildup=df_playerstats["us_xGBuildup"][i],
                xGChain_90=df_playerstats["us_xGChain_90"][i],
                xGBuildup_90=df_playerstats["us_xGBuildup_90"][i],
                last_third_passes=df_playerstats["fb_last_third_passes"][i],
                ppa=df_playerstats["fb_PPA"][i],
                crosses_pa=df_playerstats["fb_CrsPA"][i],
                progresive_passes=df_playerstats["fb_progresive_passes"][i],
                progresive_passes_attempted=df_playerstats["fb_progresive_passes_Att"][
                    i
                ],
                live_passes=df_playerstats["fb_Pass_Types_Live"][i],
                dead_passes=df_playerstats["fb_Pass_Types_Dead"][i],
                free_kick_passes=df_playerstats["fb_Pass_Types_FK"][i],
                to_back_passes=df_playerstats["fb_Pass_Types_TB"][i],
                pressed_passes=df_playerstats["fb_Pass_Types_Press"][i],
                swap_passes=df_playerstats["fb_Pass_Types_Sw"][i],
                crosses=df_playerstats["fb_Pass_Types_Crs"][i],
                corner_kicks=df_playerstats["fb_Pass_Types_CK"][i],
                corner_kicks_in=df_playerstats["fb_Corner_Kicks_In"][i],
                corner_kicks_out=df_playerstats["fb_Corner_Kicks_Out"][i],
                corner_kicks_straight=df_playerstats["fb_Corner_Kicks_Str"][i],
                ground_passes=df_playerstats["fb_Height_Ground"][i],
                low_passes=df_playerstats["fb_Height_Low"][i],
                high_passes=df_playerstats["fb_Height_High"][i],
                left_foot_passes=df_playerstats["fb_Body_Parts_Left"][i],
                right_foot_passes=df_playerstats["fb_Body_Parts_Right"][i],
                head_passes=df_playerstats["fb_Body_Parts_Head"][i],
                throw_in_passes=df_playerstats["fb_Body_Parts_TI"][i],
                other_body_parts_passes=df_playerstats["fb_Body_Parts_Other"][i],
                offsides_passes=df_playerstats["fb_Outcomes_Offsides"][i],
                out_off_bound_passes=df_playerstats["fb_Outcomes_Out"][i],
                intercepted_passes=df_playerstats["fb_Outcomes_Int"][i],
                blocked_passes=df_playerstats["fb_Outcomes_Blocks"][i],
                sca=df_playerstats["fb_SCA_SCA"][i],
                sca_90=df_playerstats["fb_SCA_SCA90"][i],
                sca_live_pass=df_playerstats["fb_SCA_Types_PassLive"][i],
                sca_dead_pass=df_playerstats["fb_SCA_Types_PassDead"][i],
                sca_dribbling=df_playerstats["fb_SCA_Types_Drib"][i],
                sca_another_shoot=df_playerstats["fb_SCA_Types_Sh"][i],
                sca_foul_drawn=df_playerstats["fb_SCA_Types_Fld"][i],
                sca_defensive_action=df_playerstats["fb_SCA_Types_Def"][i],
                gca=df_playerstats["fb_GCA_GCA"][i],
                gca_90=df_playerstats["fb_GCA_GCA90"][i],
                gca_live_pass=df_playerstats["fb_GCA_Types_PassLive"][i],
                gca_dead_pass=df_playerstats["fb_GCA_Types_PassDead"][i],
                gca_dribbling=df_playerstats["fb_GCA_Types_Drib"][i],
                gca_another_shoot=df_playerstats["fb_GCA_Types_Sh"][i],
                gca_foul_drawn=df_playerstats["fb_GCA_Types_Fld"][i],
                gca_defensive_action=df_playerstats["fb_GCA_Types_Def"][i],
                tackles=df_playerstats["fb_Tackles_Tkl"][i],
                tackles_wins=df_playerstats["fb_Tackles_TklW"][i],
                tackles_def_third=df_playerstats["fb_Tackles_Def_3rd"][i],
                tackles_mid_third=df_playerstats["fb_Tackles_Mid_3rd"][i],
                tackles_att_third=df_playerstats["fb_Tackles_Att_3rd"][i],
                tackles_vs_dribbles_wins=df_playerstats["fb_vs_Dribbles_Tkl"][i],
                tackles_vs_dribbles_attempted=df_playerstats["fb_vs_Dribbles_Att"][i],
                perc_tackles_vs_dribbles=df_playerstats["fb_vs_Dribbles_Tkl_perc"][i],
                pressures=df_playerstats["fb_Pressures_Press"][i],
                pressures_success=df_playerstats["fb_Pressures_Succ"][i],
                perc_pressures_success=df_playerstats["fb_Pressures_perc"][i],
                pressures_def_third=df_playerstats["fb_Pressures_Def_3rd"][i],
                pressures_mid_third=df_playerstats["fb_Pressures_Mid_3rd"][i],
                pressures_att_third=df_playerstats["fb_Pressures_Att_3rd"][i],
                blocks=df_playerstats["fb_Blocks"][i],
                blocks_shoots=df_playerstats["fb_Blocks_Sh"][i],
                blocks_shoots_on_target=df_playerstats["fb_Blocks_ShSv"][i],
                blocks_passes=df_playerstats["fb_Blocks_Pass"][i],
                interceptions=df_playerstats["fb_Interceptions"][i],
                tackles_plus_interceptions=df_playerstats["fb_Tkl_plus_Int"][i],
                clearances=df_playerstats["fb_Clearances"][i],
                errors_to_rival_shoot=df_playerstats["fb_Errors"][i],
                aerial_duels_won=df_playerstats["fb_Aerial_Duels_Won"][i],
                aerial_duels_lost=df_playerstats["fb_Aerial_Duels_Lost"][i],
                perc_aerial_duels_won=df_playerstats["fb_Aerial_Duels_Won_perc"][i],
                touches=df_playerstats["fb_Touches"][i],
                touches_def_box=df_playerstats["fb_Touches_Def_Pen"][i],
                touches_def_third=df_playerstats["fb_Touches_Def_3rd"][i],
                touches_mid_third=df_playerstats["fb_Touches_Mid_3rd"][i],
                touches_att_third=df_playerstats["fb_Touches_Att_3rd"][i],
                touches_att_box=df_playerstats["fb_Touches_Att_Pen"][i],
                dribbles_success=df_playerstats["fb_Dribbles_Succ"][i],
                dribbles_attempted=df_playerstats["fb_Dribbles_Att"][i],
                perc_dribbles_success=df_playerstats["fb_Dribbles_Succ_perc"][i],
                number_players_dribbled=df_playerstats["fb_Dribbles_number_Pl"][i],
                dribbles_megs=df_playerstats["fb_Dribbles_Megs"][i],
                carries=df_playerstats["fb_Carries"][i],
                distance_carries=df_playerstats["fb_Carries_TotDist"][i],
                progressive_distance_carries=df_playerstats["fb_Carries_PrgDist"][i],
                progressive_carries=df_playerstats["fb_Carries_Prog"][i],
                carries_last_third=df_playerstats["fb_Carries_last_third"][i],
                carries_to_att_box=df_playerstats["fb_Carries_CPA"][i],
                carries_missed=df_playerstats["fb_Carries_Mis"][i],
                carries_intercepted=df_playerstats["fb_Carries_Dis"][i],
                receiving_target=df_playerstats["fb_Receiving_Targ"][i],
                receiving_target_success=df_playerstats["fb_Receiving_Rec"][i],
                perc_receiving_target_success=df_playerstats["fb_Receiving_Rec_perc"][
                    i
                ],
                receiving_target_progressive=df_playerstats["fb_Receiving_Prog"][i],
                yellow_cards=df_playerstats["fb_CrdY"][i],
                red_cards=df_playerstats["fb_CrdR"][i],
                double_yellow_cards=df_playerstats["fb_Performance_2CrdY"][i],
                fouls=df_playerstats["fb_Performance_Fouls"][i],
                fouls_drawn=df_playerstats["fb_Performance_Fouls_drawn"][i],
                offsides=df_playerstats["fb_Performance_Offsides"][i],
                penalties_wons=df_playerstats["fb_Performance_PKwon"][i],
                penalties_conceded=df_playerstats["fb_Performance_PKconceded"][i],
                own_goals=df_playerstats["fb_Performance_OG"][i],
                recoveries=df_playerstats["fb_Performance_Recov"][i],
            )

        print("Guardando información de los porteros en la base de datos")
        for i in tqdm(range(len(df_goalkeeperstats))):
            GoalkeeperStats.objects.get_or_create(
                player=Player.objects.get(id=df_goalkeeperstats["id"][i]),
                extraction_date=scrape_date,
                season=df_goalkeeperstats["fb_season"][i],
                team=df_goalkeeperstats["fb_team"][i],
                team_date_joined=df_goalkeeperstats["tm_date_joined"][i],
                team_contract_expires=df_goalkeeperstats["tm_contract_expires"][i],
                competition=df_goalkeeperstats["fb_comp"][i],
                salary=df_goalkeeperstats["ca_salary"][i],
                current_value=df_goalkeeperstats["tm_current_value"][i],
                matches_played=df_goalkeeperstats["fb_playing_time_MP"][i],
                matches_starts=df_goalkeeperstats["fb_playing_time_starts"][i],
                minutes_played=df_goalkeeperstats["fb_playing_time_min"][i],
                playing_time_90s=df_goalkeeperstats["fb_playing_time_90s"][i],
                assists=df_goalkeeperstats["fb_Ast"][i],
                expected_assists=df_goalkeeperstats["fb_xA"][i],
                assists_90=df_goalkeeperstats["fb_Ast_90"][i],
                expected_assists_90=df_goalkeeperstats["fb_xA_90"][i],
                goals_against=df_goalkeeperstats["fb_GA"][i],
                goals_against_90=df_goalkeeperstats["fb_GA_90"][i],
                shoots_on_target_against=df_goalkeeperstats["fb_SoTA"][i],
                saves=df_goalkeeperstats["fb_saves"][i],
                perc_saves=df_goalkeeperstats["fb_save_perc"][i],
                clear_scores=df_goalkeeperstats["fb_CS"][i],
                perc_clear_scores=df_goalkeeperstats["fb_CS_perc"][i],
                penalty_against=df_goalkeeperstats["fb_PK_against"][i],
                penalty_saves=df_goalkeeperstats["fb_PK_saves"][i],
                perc_penalty_saves=df_goalkeeperstats["fb_PK_saves_perc"][i],
                psxg=df_goalkeeperstats["fb_PSxG"][i],
                psxg_per_shoots=df_goalkeeperstats["fb_PSxG_vs_SoT"][i],
                psxg_diference=df_goalkeeperstats["fb_PSxG_dif"][i],
                launches_completed=df_goalkeeperstats["fb_Launched_Cmp"][i],
                launches_attempted=df_goalkeeperstats["fb_Launched_Att"][i],
                perc_launches_completed=df_goalkeeperstats["fb_Launched_Cmp_perc"][i],
                passes_attempted=df_goalkeeperstats["fb_Passes_Att"][i],
                average_lenght_passes=df_goalkeeperstats["fb_Passes_AvgLen"][i],
                goal_kicks_attempted=df_goalkeeperstats["fb_Goal_Kicks_Att"][i],
                perc_goal_kicks_completed=df_goalkeeperstats[
                    "fb_Goal_Kicks_Launch_perc"
                ][i],
                average_lenght_goal_kick=df_goalkeeperstats["fb_Goal_Kicks_AvgLen"][i],
                opponent_crosses=df_goalkeeperstats["fb_Crosses_Opp"][i],
                opponent_crosses_stopped=df_goalkeeperstats["fb_Crosses_Stp"][i],
                perc_opponent_crosses_stopped=df_goalkeeperstats["fb_Crosses_Stp_perc"][
                    i
                ],
                sweeper_opa=df_goalkeeperstats["fb_Sweeper_OPA"][i],
                sweeper_opa_90=df_goalkeeperstats["fb_Sweeper_OPA_90"][i],
                average_distance_sweeper=df_goalkeeperstats["fb_Sweeper_AvgDist"][i],
                yellow_cards=df_goalkeeperstats["fb_CrdY"][i],
                red_cards=df_goalkeeperstats["fb_CrdR"][i],
            )
        self.stdout.write("Job completado sin errores")
