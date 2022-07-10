from django.db import models
from django.utils import timezone

import uuid


class ScrapeJob(models.Model):
    # Select para el estatus del scrape
    OK = "OK"
    ERROR = "KO"
    EN_PROCESO = "IN"
    STATE_CHOICES = [
        (OK, "Completado"),
        (ERROR, "Con errores"),
        (EN_PROCESO, "En proceso"),
    ]

    # Opciones para la web de origen
    FBREF = "FB"
    UNDERSTAT = "US"
    TRANSFERMARKT = "TM"
    CAPOLOGY = "CA"
    ORIGIN_CHOICES = [
        (FBREF, "FB"),
        (UNDERSTAT, "US"),
        (TRANSFERMARKT, "TM"),
        (CAPOLOGY, "CA"),
    ]

    scrape_job_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    created_date = models.DateTimeField(default=timezone.now)
    mode = models.CharField(max_length=20)
    origin = models.CharField(max_length=2, choices=ORIGIN_CHOICES, default=FBREF)
    scraped_from = models.CharField(max_length=50)
    season_from = models.CharField(max_length=30)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=EN_PROCESO)
    number_errors = models.IntegerField(default=0, blank=True)
    completed_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Web Scraping Job"
        verbose_name_plural = "Web Scraping Jobs"

    def __str__(self):
        return "{} - {}".format(self.scraped_from, self.season_from)


class PlayerUnderstat(models.Model):
    """Model definition for PlayerUnderstat."""

    us_player_id = models.IntegerField(default=0, blank=True)
    us_player_name = models.CharField(max_length=250)
    us_position = models.CharField(max_length=10)
    us_team = models.CharField(max_length=150)
    us_season = models.CharField(max_length=30)
    us_comp = models.CharField(max_length=50)
    us_key_passes = models.IntegerField(default=0, blank=True)
    us_xGChain = models.FloatField(default=0, blank=True)
    us_xGBuildup = models.FloatField(default=0, blank=True)
    us_key_passes_90 = models.FloatField(default=0, blank=True)
    us_xGChain_90 = models.FloatField(default=0, blank=True)
    us_xGBuildup_90 = models.FloatField(default=0, blank=True)
    scrape_job = models.ForeignKey("ScrapeJob", on_delete=models.CASCADE)
    created_data = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Player data from Understat"
        verbose_name_plural = "Players data from Understat"

        constraints = [
            models.UniqueConstraint(
                fields=["us_player_id", "us_season", "us_team"],
                name="unique_player_id_season_team_combination_us",
            )
        ]

    def __str__(self):
        return "{} - {} ({})".format(self.us_player_name, self.us_team, self.us_season)


class PlayerFbrefGK(models.Model):
    fb_player_id = models.IntegerField(blank=False)
    fb_player_name = models.CharField(max_length=120, blank=False)
    fb_season = models.CharField(max_length=30)
    fb_nation = models.CharField(max_length=3)
    fb_pos = models.CharField(max_length=10, verbose_name="fb_position")
    fb_team = models.CharField(max_length=50, blank=True)
    fb_comp = models.CharField(max_length=50, verbose_name="fb_competition")
    fb_born = models.DateField(blank=True)
    fb_playing_time_MP = models.IntegerField(default=0, blank=True)
    fb_playing_time_starts = models.IntegerField(default=0, blank=True)
    fb_playing_time_min = models.IntegerField(default=0, blank=True)
    fb_playing_time_90s = models.FloatField(default=0, blank=True)
    fb_Gls = models.IntegerField(default=0, blank=True)
    fb_Ast = models.IntegerField(default=0, blank=True)
    fb_G_minus_PK = models.IntegerField(default=0, blank=True)
    fb_PK = models.IntegerField(default=0, blank=True)
    fb_PKatt = models.IntegerField(default=0, blank=True)
    fb_CrdY = models.IntegerField(default=0, blank=True)
    fb_CrdR = models.IntegerField(default=0, blank=True)
    fb_Gls_90 = models.FloatField(default=0, blank=True)
    fb_Ast_90 = models.FloatField(default=0, blank=True)
    fb_G_plus_A_90 = models.FloatField(default=0, blank=True)
    fb_G_plus_A_minus_PK = models.IntegerField(default=0, blank=True)
    fb_xG = models.FloatField(default=0, blank=True)
    fb_npxG = models.FloatField(default=0, blank=True)
    fb_xA = models.FloatField(default=0, blank=True)
    fb_npxG_plus_xA = models.FloatField(default=0, blank=True)
    fb_xG_90 = models.FloatField(default=0, blank=True)
    fb_xA_90 = models.FloatField(default=0, blank=True)
    fb_xG_plus_xA_90 = models.FloatField(default=0, blank=True)
    fb_npxG_90 = models.FloatField(default=0, blank=True)
    fb_npxG_plus_xA_90 = models.FloatField(default=0, blank=True)
    fb_GA = models.IntegerField(default=0, blank=True)
    fb_GA_90 = models.FloatField(default=0, blank=True)
    fb_SoTA = models.IntegerField(default=0, blank=True)
    fb_saves = models.IntegerField(default=0, blank=True)
    fb_save_perc = models.FloatField(default=0, blank=True)
    fb_W = models.IntegerField(default=0, blank=True)
    fb_D = models.IntegerField(default=0, blank=True)
    fb_L = models.IntegerField(default=0, blank=True)
    fb_CS = models.IntegerField(default=0, blank=True)
    fb_CS_perc = models.FloatField(default=0, blank=True)
    fb_PK_against = models.IntegerField(default=0, blank=True)
    fb_PK_saves = models.IntegerField(default=0, blank=True)
    fb_PK_m = models.FloatField(default=0, blank=True)
    fb_PSxG = models.FloatField(default=0, blank=True)
    fb_PSxG_vs_SoT = models.FloatField(default=0, blank=True)
    fb_PSxG_plus_vs_minus = models.FloatField(default=0, blank=True)
    fb_Launched_Cmp = models.IntegerField(default=0, blank=True)
    fb_Launched_Att = models.IntegerField(default=0, blank=True)
    fb_Launched_Cmp_perc = models.FloatField(default=0, blank=True)
    fb_Passes_Att = models.IntegerField(default=0, blank=True)
    fb_Passes_Thr = models.IntegerField(default=0, blank=True)
    fb_Passes_Launch_perc = models.FloatField(default=0, blank=True)
    fb_Passes_AvgLen = models.FloatField(default=0, blank=True)
    fb_Goal_Kicks_Att = models.IntegerField(default=0, blank=True)
    fb_Goal_Kicks_Launch_perc = models.FloatField(default=0, blank=True)
    fb_Goal_Kicks_AvgLen = models.FloatField(default=0, blank=True)
    fb_Crosses_Opp = models.IntegerField(default=0, blank=True)
    fb_Crosses_Stp = models.IntegerField(default=0, blank=True)
    fb_Crosses_Stp_perc = models.FloatField(default=0, blank=True)
    fb_Sweeper_OPA = models.FloatField(default=0, blank=True)
    fb_Sweeper_OPA_90 = models.FloatField(default=0, blank=True)
    fb_Sweeper_AvgDist = models.FloatField(default=0, blank=True)
    scrape_job = models.ForeignKey("ScrapeJob", on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Goalkeeper data from FBRef"
        verbose_name_plural = "Goalkeepers data from FBRef"

        constraints = [
            models.UniqueConstraint(
                fields=["fb_player_id", "fb_season", "fb_team"],
                name="unique_player_id_season_team_combination_fbref_gk",
            )
        ]

    def __str__(self):
        return "{} - {} ({})".format(self.fb_player_name, self.fb_team, self.fb_season)

    @property
    def age(self):
        return (
            timezone.now().year
            - self.fb_born.year
            - (
                (timezone.now().month, timezone.now().day)
                < (self.fb_born.month, self.fb_born.day)
            )
        )


class PlayerFbref(models.Model):
    fb_player_id = models.IntegerField(blank=False)
    fb_player_name = models.CharField(max_length=120, blank=False)
    fb_season = models.CharField(max_length=30)
    fb_nation = models.CharField(max_length=3)
    fb_pos = models.CharField(max_length=10, verbose_name="fb_position")
    fb_team = models.CharField(max_length=50, blank=True)
    fb_comp = models.CharField(max_length=50, verbose_name="fb_competition")
    fb_born = models.DateField(blank=True)
    fb_playing_time_MP = models.IntegerField(default=0, blank=True)
    fb_playing_time_starts = models.IntegerField(default=0, blank=True)
    fb_playing_time_min = models.IntegerField(default=0, blank=True)
    fb_playing_time_90s = models.FloatField(default=0, blank=True)
    fb_Gls = models.IntegerField(default=0, blank=True)
    fb_Ast = models.IntegerField(default=0, blank=True)
    fb_G_minus_PK = models.IntegerField(default=0, blank=True)
    fb_PK = models.IntegerField(default=0, blank=True)
    fb_PKatt = models.IntegerField(default=0, blank=True)
    fb_CrdY = models.IntegerField(default=0, blank=True)
    fb_CrdR = models.IntegerField(default=0, blank=True)
    fb_Gls_90 = models.FloatField(default=0, blank=True)
    fb_Ast_90 = models.FloatField(default=0, blank=True)
    fb_G_plus_A_90 = models.FloatField(default=0, blank=True)
    fb_G_plus_A_minus_PK = models.IntegerField(default=0, blank=True)
    fb_xG = models.FloatField(default=0, blank=True)
    fb_npxG = models.FloatField(default=0, blank=True)
    fb_xA = models.FloatField(default=0, blank=True)
    fb_npxG_plus_xA = models.FloatField(default=0, blank=True)
    fb_xG_90 = models.FloatField(default=0, blank=True)
    fb_xA_90 = models.FloatField(default=0, blank=True)
    fb_xG_plus_xA_90 = models.FloatField(default=0, blank=True)
    fb_npxG_90 = models.FloatField(default=0, blank=True)
    fb_npxG_plus_xA_90 = models.FloatField(default=0, blank=True)
    fb_Sh = models.IntegerField(default=0, blank=True)
    fb_SoT = models.IntegerField(default=0, blank=True)
    fb_SoT_perc = models.FloatField(default=0, blank=True)
    fb_Sh_90 = models.FloatField(default=0, blank=True)
    fb_SoT_90 = models.FloatField(default=0, blank=True)
    fb_G_vs_Sh = models.FloatField(default=0, blank=True)
    fb_G_vs_SoT = models.FloatField(default=0, blank=True)
    fb_Dist = models.IntegerField(default=0, blank=True)
    fb_FK = models.IntegerField(default=0, blank=True)
    fb_PK = models.IntegerField(default=0, blank=True)
    fb_PKatt = models.IntegerField(default=0, blank=True)
    fb_npxG_vs_Sh = models.FloatField(default=0, blank=True)
    fb_G_minus_xG = models.FloatField(default=0, blank=True)
    fb_npxG_minus_xG = models.FloatField(default=0, blank=True)
    fb_passes_Cmp = models.IntegerField(default=0, blank=True)
    fb_passes_Att = models.IntegerField(default=0, blank=True)
    fb_passes_Cmp_perc = models.FloatField(default=0, blank=True)
    fb_passes_TotDist = models.IntegerField(default=0, blank=True)
    fb_passes_PrgDist = models.IntegerField(default=0, blank=True)
    fb_passes_Short_Cmp = models.IntegerField(default=0, blank=True)
    fb_passes_Short_Att = models.IntegerField(default=0, blank=True)
    fb_passes_Short_Cmp_perc = models.FloatField(default=0, blank=True)
    fb_passes_Medium_Cmp = models.IntegerField(default=0, blank=True)
    fb_passes_Medium_Att = models.IntegerField(default=0, blank=True)
    fb_passes_Medium_Cmp_perc = models.FloatField(default=0, blank=True)
    fb_passes_Long_Cmp = models.IntegerField(default=0, blank=True)
    fb_passes_Long_Att = models.IntegerField(default=0, blank=True)
    fb_passes_Long_Cmp_perc = models.FloatField(default=0, blank=True)
    fb_A_minus_xA = models.FloatField(default=0, blank=True)
    fb_key_passes = models.IntegerField(default=0, blank=True)
    fb_last_third_passes = models.IntegerField(default=0, blank=True)
    fb_PPA = models.IntegerField(default=0, blank=True)
    fb_CrsPA = models.IntegerField(default=0, blank=True)
    fb_progresive_passes = models.IntegerField(default=0, blank=True)
    fb_progresive_passes_Att = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_Live = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_Dead = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_FK = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_TB = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_Press = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_Sw = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_Crs = models.IntegerField(default=0, blank=True)
    fb_Pass_Types_CK = models.IntegerField(default=0, blank=True)
    fb_Corner_Kicks_In = models.IntegerField(default=0, blank=True)
    fb_Corner_Kicks_Out = models.IntegerField(default=0, blank=True)
    fb_Corner_Kicks_Str = models.IntegerField(default=0, blank=True)
    fb_Height_Ground = models.IntegerField(default=0, blank=True)
    fb_Height_Low = models.IntegerField(default=0, blank=True)
    fb_Height_High = models.IntegerField(default=0, blank=True)
    fb_Body_Parts_Left = models.IntegerField(default=0, blank=True)
    fb_Body_Parts_Right = models.IntegerField(default=0, blank=True)
    fb_Body_Parts_Head = models.IntegerField(default=0, blank=True)
    fb_Body_Parts_TI = models.IntegerField(default=0, blank=True)
    fb_Body_Parts_Other = models.IntegerField(default=0, blank=True)
    fb_Outcomes_Cmp = models.IntegerField(default=0, blank=True)
    fb_Outcomes_Offsides = models.IntegerField(default=0, blank=True)
    fb_Outcomes_Out = models.IntegerField(default=0, blank=True)
    fb_Outcomes_Int = models.IntegerField(default=0, blank=True)
    fb_Outcomes_Blocks = models.IntegerField(default=0, blank=True)
    fb_SCA_SCA = models.IntegerField(default=0, blank=True)
    fb_SCA_SCA90 = models.FloatField(default=0, blank=True)
    fb_SCA_Types_PassLive = models.IntegerField(default=0, blank=True)
    fb_SCA_Types_PassDead = models.IntegerField(default=0, blank=True)
    fb_SCA_Types_Drib = models.IntegerField(default=0, blank=True)
    fb_SCA_Types_Sh = models.IntegerField(default=0, blank=True)
    fb_SCA_Types_Fld = models.IntegerField(default=0, blank=True)
    fb_SCA_Types_Def = models.IntegerField(default=0, blank=True)
    fb_GCA_GCA = models.IntegerField(default=0, blank=True)
    fb_GCA_GCA90 = models.FloatField(default=0, blank=True)
    fb_GCA_Types_PassLive = models.IntegerField(default=0, blank=True)
    fb_GCA_Types_PassDead = models.IntegerField(default=0, blank=True)
    fb_GCA_Types_Drib = models.IntegerField(default=0, blank=True)
    fb_GCA_Types_Sh = models.IntegerField(default=0, blank=True)
    fb_GCA_Types_Fld = models.IntegerField(default=0, blank=True)
    fb_GCA_Types_Def = models.IntegerField(default=0, blank=True)
    fb_Tackles_Tkl = models.IntegerField(default=0, blank=True)
    fb_Tackles_TklW = models.IntegerField(default=0, blank=True)
    fb_Tackles_Def_3rd = models.IntegerField(default=0, blank=True)
    fb_Tackles_Mid_3rd = models.IntegerField(default=0, blank=True)
    fb_Tackles_Att_3rd = models.IntegerField(default=0, blank=True)
    fb_vs_Dribbles_Tkl = models.IntegerField(default=0, blank=True)
    fb_vs_Dribbles_Att = models.IntegerField(default=0, blank=True)
    fb_vs_Dribbles_Tkl_perc = models.FloatField(default=0, blank=True)
    fb_vs_Dribbles_Past = models.IntegerField(default=0, blank=True)
    fb_Pressures_Press = models.IntegerField(default=0, blank=True)
    fb_Pressures_Succ = models.IntegerField(default=0, blank=True)
    fb_Pressures_perc = models.FloatField(default=0, blank=True)
    fb_Pressures_Def_3rd = models.IntegerField(default=0, blank=True)
    fb_Pressures_Mid_3rd = models.IntegerField(default=0, blank=True)
    fb_Pressures_Att_3rd = models.IntegerField(default=0, blank=True)
    fb_Blocks = models.IntegerField(default=0, blank=True)
    fb_Blocks_Sh = models.IntegerField(default=0, blank=True)
    fb_Blocks_ShSv = models.IntegerField(default=0, blank=True)
    fb_Blocks_Pass = models.IntegerField(default=0, blank=True)
    fb_Interceptions = models.IntegerField(default=0, blank=True)
    fb_Tkl_plus_Int = models.IntegerField(default=0, blank=True)
    fb_Clearances = models.IntegerField(default=0, blank=True)
    fb_Errors = models.IntegerField(default=0, blank=True)
    fb_Touches = models.IntegerField(default=0, blank=True)
    fb_Touches_Def_Pen = models.IntegerField(default=0, blank=True)
    fb_Touches_Def_3rd = models.IntegerField(default=0, blank=True)
    fb_Touches_Mid_3rd = models.IntegerField(default=0, blank=True)
    fb_Touches_Att_3rd = models.IntegerField(default=0, blank=True)
    fb_Touches_Att_Pen = models.IntegerField(default=0, blank=True)
    fb_Touches_Live = models.IntegerField(default=0, blank=True)
    fb_Dribbles_Succ = models.IntegerField(default=0, blank=True)
    fb_Dribbles_Att = models.IntegerField(default=0, blank=True)
    fb_Dribbles_Succ_perc = models.FloatField(default=0, blank=True)
    fb_Dribbles_number_Pl = models.IntegerField(default=0, blank=True)
    fb_Dribbles_Megs = models.IntegerField(default=0, blank=True)
    fb_Carries = models.IntegerField(default=0, blank=True)
    fb_Carries_TotDist = models.IntegerField(default=0, blank=True)
    fb_Carries_PrgDist = models.IntegerField(default=0, blank=True)
    fb_Carries_Prog = models.IntegerField(default=0, blank=True)
    fb_Carries_last_third = models.IntegerField(default=0, blank=True)
    fb_Carries_CPA = models.IntegerField(default=0, blank=True)
    fb_Carries_Mis = models.IntegerField(default=0, blank=True)
    fb_Carries_Dis = models.IntegerField(default=0, blank=True)
    fb_Receiving_Targ = models.IntegerField(default=0, blank=True)
    fb_Receiving_Rec = models.IntegerField(default=0, blank=True)
    fb_Receiving_Rec_perc = models.FloatField(default=0, blank=True)
    fb_Receiving_Prog = models.IntegerField(default=0, blank=True)
    fb_Playing_Time_Mn_vs_MP = models.IntegerField(default=0, blank=True)
    fb_Playing_Time_Min_perc = models.FloatField(default=0, blank=True)
    fb_Starts_Min_vs_Start = models.IntegerField(default=0, blank=True)
    fb_Starts_Compl = models.IntegerField(default=0, blank=True)
    fb_Subs_Subs = models.IntegerField(default=0, blank=True)
    fb_Subs_Mn_vs_Sub = models.IntegerField(default=0, blank=True)
    fb_Subs_unSub = models.IntegerField(default=0, blank=True)
    fb_Team_Success_PPM = models.FloatField(default=0, blank=True)
    fb_Team_Success_onG = models.IntegerField(default=0, blank=True)
    fb_Team_Success_onGA = models.IntegerField(default=0, blank=True)
    fb_Team_Success_dif = models.FloatField(default=0, blank=True)
    fb_Team_Success_dif_90 = models.FloatField(default=0, blank=True)
    fb_Team_Success_On_Off = models.FloatField(default=0, blank=True)
    fb_Team_Success_xG_onxG = models.FloatField(default=0, blank=True)
    fb_Team_Success_xG_onxGA = models.FloatField(default=0, blank=True)
    fb_Team_Success_xG_xGdif = models.FloatField(default=0, blank=True)
    fb_Team_Success_xG_xGdif_90 = models.FloatField(default=0, blank=True)
    fb_Team_Success_xG_On_Off = models.FloatField(default=0, blank=True)
    fb_Performance_2CrdY = models.IntegerField(default=0, blank=True)
    fb_Performance_Fouls = models.IntegerField(default=0, blank=True)
    fb_Performance_Fouls_drawn = models.IntegerField(default=0, blank=True)
    fb_Performance_Offsides = models.IntegerField(default=0, blank=True)
    fb_Performance_Cross = models.IntegerField(default=0, blank=True)
    fb_Performance_Interceptions = models.IntegerField(default=0, blank=True)
    fb_Performance_TklW = models.IntegerField(default=0, blank=True)
    fb_Performance_PKwon = models.IntegerField(default=0, blank=True)
    fb_Performance_PKconceded = models.IntegerField(default=0, blank=True)
    fb_Performance_OG = models.IntegerField(default=0, blank=True)
    fb_Performance_Recov = models.IntegerField(default=0, blank=True)
    fb_Aerial_Duels_Won = models.IntegerField(default=0, blank=True)
    fb_Aerial_Duels_Lost = models.IntegerField(default=0, blank=True)
    fb_Aerial_Duels_Won_perc = models.FloatField(default=0, blank=True)
    scrape_job = models.ForeignKey("ScrapeJob", on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Player data from FBRef"
        verbose_name_plural = "Players data from FBRef"

        constraints = [
            models.UniqueConstraint(
                fields=["fb_player_id", "fb_season", "fb_team"],
                name="unique_player_id_season_team_combination_fbref_players",
            )
        ]

    def __str__(self):
        return "{} - {} ({})".format(self.fb_player_name, self.fb_team, self.fb_season)

    @property
    def age(self):
        return (
            timezone.now().year
            - self.fb_born.year
            - (
                (timezone.now().month, timezone.now().day)
                < (self.fb_born.month, self.fb_born.day)
            )
        )


class PlayerCapology(models.Model):
    ca_player_id = models.CharField(max_length=150, blank=False)
    ca_player_name = models.CharField(max_length=120, blank=False)
    ca_salary = models.DecimalField(max_digits=12, decimal_places=2)
    ca_expiration = models.DateField(blank=True)
    ca_country = models.CharField(max_length=100, blank=False)
    ca_team = models.CharField(max_length=100)
    ca_season = models.CharField(max_length=30, blank=False)
    ca_comp = models.CharField(max_length=50, blank=False)
    scrape_job = models.ForeignKey("ScrapeJob", on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Player data from Capology"
        verbose_name_plural = "Players data from Capology"

    def __str__(self):
        return "{} - {} ({})".format(self.ca_player_name, self.ca_team, self.ca_season)


class PlayerTransfermarkt(models.Model):
    tm_player_id = models.IntegerField(blank=False)
    tm_player_name = models.CharField(max_length=120, blank=False)
    tm_comp = models.CharField(max_length=50, blank=False)
    tm_player_image_url = models.URLField()
    tm_current_value = models.DecimalField(max_digits=12, decimal_places=2)
    tm_birthdate = models.DateField(blank=True, null=True)
    tm_yearbirthdate = models.CharField(max_length=4, blank=True)
    tm_citizenship = models.CharField(max_length=100, blank=True)
    tm_position = models.CharField(max_length=60, blank=True)
    tm_height = models.CharField(max_length=50, blank=True)
    tm_foot = models.CharField(max_length=20, blank=True)
    tm_current_club = models.CharField(max_length=100)
    tm_date_joined = models.DateField(blank=True, null=True)
    tm_contract_expires = models.DateField(blank=True, null=True)
    scrape_job = models.ForeignKey("ScrapeJob", on_delete=models.CASCADE)
    created_data = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Player data from Transfermarkt"
        verbose_name_plural = "Players data from Transfermarkt"

    def __str__(self):
        return "{} - {}".format(self.tm_player_name, self.tm_current_club)

    @property
    def age(self):
        return (
            timezone.now().year
            - self.tm_birthdate.year
            - (
                (timezone.now().month, timezone.now().day)
                < (self.tm_birthdate.month, self.tm_birthdate.day)
            )
        )
