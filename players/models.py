from django.db import models
from django.urls import reverse
from django.utils import timezone

import uuid


class Player(models.Model):
    """Model definition for Player."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(
        max_length=120, blank=False, verbose_name="Nombre del jugador"
    )
    also_named = models.CharField(
        max_length=255, blank=True, default="", verbose_name="También llamado"
    )
    dob = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    citizenship = models.CharField(
        max_length=80, blank=True, verbose_name="País de origen"
    )
    height = models.FloatField(blank=True, verbose_name="Altura")
    foot = models.CharField(max_length=10, blank=True, verbose_name="Pie")
    position = models.CharField(max_length=50, verbose_name="Posición")
    position_norm = models.CharField(
        max_length=30, verbose_name="Posición normalizada"
    )  # TODO Sacar a una tabla de posiciones normalizadas?
    image = models.URLField(
        max_length=255,
        verbose_name="Foto del jugador",
        default="https://img.a.transfermarkt.technology/portrait/header/default.jpg",
    )
    id_fbref = models.CharField(max_length=30, blank=True)
    id_understat = models.CharField(max_length=30, blank=True)
    id_transfermarkt = models.CharField(max_length=30, blank=True)
    id_capology = models.CharField(max_length=150, blank=True)

    class Meta:
        """Meta definition for Player."""

        verbose_name = "Jugador"
        verbose_name_plural = "Jugadores"

    def __str__(self):
        """Unicode representation of Player."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Player."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Player."""
        # return reverse("scrapes_detail", args=[str(self.pk)])
        pass

    @property
    def age(self):
        return (
            timezone.now().year
            - self.dob.year
            - (
                (timezone.now().month, timezone.now().day)
                < (self.dob.month, self.dob.day)
            )
        )

    def get_current_player_scoring_by_index(self):
        current_scoring = Scoring.objects.filter(player=self.pk).latest(
            "calculate_date"
        )
        return current_scoring.scoring


class Index(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    index_name = models.CharField(
        max_length=50, blank=False, verbose_name="Nombre del Index"
    )
    description = models.TextField(blank=True, verbose_name="Descripción corta")
    position_norm = models.CharField(
        max_length=30, verbose_name="Posición normalizada"
    )  # TODO Sacar a una tabla de posiciones normalizadas?
    index_data = models.JSONField(verbose_name="Métricas y pesos del Index")
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        """Meta definition for Index."""

        verbose_name = "Index"
        verbose_name_plural = "Indexes"

    def __str__(self):
        """Unicode representation of Index."""
        return "{} - ({})".format(self.index_name, self.position_norm)

    def save(self):
        """Save method for Index."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Index."""
        return ""


class PlayerStats(models.Model):
    """Model definition for PlayerStats."""

    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Jugador")
    extraction_date = models.DateTimeField(
        verbose_name="Fecha de extracción"
    )  # Sale del Scrape job para comparar
    season = models.CharField(max_length=30, verbose_name="Temporada")  # fb_season
    team = models.CharField(max_length=50, blank=True, verbose_name="Equipo")  # fb_team
    team_date_joined = models.DateField(
        blank=True, null=True, verbose_name="Fecha de inicio de contrato"
    )  # tm_date_joined
    team_contract_expires = models.DateField(
        blank=True, null=True, verbose_name="Fecha de fin de contrato"
    )  # tm_contract_expires
    competition = models.CharField(max_length=50, verbose_name="Competición")  # fb_comp
    ca_salary = models.DecimalField(max_digits=12, decimal_places=2)  # ca_salary
    tm_current_value = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # tm_current_value
    matches_played = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos jugados"
    )  # fb_playing_time_MP
    matches_starts = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos titular"
    )  # fb_playing_time_starts
    minutes_played = models.IntegerField(
        default=0, blank=True, verbose_name="Minutos jugados"
    )  # fb_playing_time_min
    minutes_per_match = models.IntegerField(
        default=0, blank=True, verbose_name="Minutos por partido"
    )  # fb_Playing_Time_Mn_vs_MP
    perc_minutes_played = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de minutos jugados"
    )  # fb_Playing_Time_Min_perc
    complete_matches_played = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos completos"
    )  # fb_Starts_Compl
    matches_as_substitute = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos jugados como suplente"
    )  # fb_Subs_Subs
    mean_minutes_starts = models.IntegerField(
        default=0, blank=True, verbose_name="Media de minutos cuando es titular"
    )  # fb_Starts_Min_vs_Start
    mean_minutes_substitute = models.IntegerField(
        default=0, blank=True, verbose_name="Media de minutos cuando es suplente"
    )  # fb_Subs_Mn_vs_Sub
    playing_time_90s = models.FloatField(
        default=0, blank=True, verbose_name="Minutos entre 90"
    )  # fb_playing_time_90s
    goals = models.IntegerField(default=0, blank=True, verbose_name="Goles")  # fb_Gls
    assists = models.IntegerField(
        default=0, blank=True, verbose_name="Asistencias"
    )  # fb_Ast
    non_penalty_goals = models.IntegerField(
        default=0, blank=True, verbose_name="Goles sin penaltis"
    )  # fb_G_minus_PK
    penalty_goals = models.IntegerField(
        default=0, blank=True, verbose_name="Penaltis marcados"
    )  # fb_PK
    penalty_shoots = models.IntegerField(
        default=0, blank=True, verbose_name="Penaltis lanzados"
    )  # fb_PKatt
    goals_plus_assists_minus_pk = models.FloatField(
        default=0, blank=True, verbose_name="Goles más asistencias sin penaltis"
    )  # fb_G_plus_A_minus_PK
    expected_goals = models.FloatField(
        default=0, blank=True, verbose_name="Goles esperados"
    )  # fb_xG
    npxg = models.FloatField(
        default=0, blank=True, verbose_name="Goles esperados sin penaltis"
    )  # fb_npxG
    expected_assists = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias esperadas"
    )  # fb_xA
    npxg_plus_expected_assists = models.FloatField(
        default=0, blank=True, verbose_name="npxG más asistencias esperadas"
    )  # fb_npxG_plus_xA
    goals_90 = models.FloatField(
        default=0, blank=True, verbose_name="Goles por 90 minutos"
    )  # fb_Gls_90
    assists_90 = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias por 90 minutos"
    )  # fb_Ast_90
    goals_plus_assists_90 = models.FloatField(
        default=0, blank=True, verbose_name="Goles y asistencias por 90 minutos"
    )  # fb_G_plus_A_90
    expected_goals_90 = models.FloatField(
        default=0, blank=True, verbose_name="Goles esperados por 90 minutos"
    )  # fb_xG_90
    expected_assists_90 = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias esperadas por 90 minutos"
    )  # fb_xA_90
    npxg_90 = models.FloatField(
        default=0,
        blank=True,
        verbose_name="Goles esperados sin penaltis por 90 minutos",
    )  # fb_npxG_90
    npxg_plus_expected_assists_90 = models.FloatField(
        default=0,
        blank=True,
        verbose_name="npxG más asistencias esperadas por 90 minutos",
    )  # fb_npxG_plus_xA_90
    assists_minus_xA = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias menos asistencias esperadas"
    )  # fb_A_minus_xA
    shoots = models.IntegerField(default=0, blank=True, verbose_name="Tiros")  # fb_Sh
    shoots_on_target = models.IntegerField(
        default=0, blank=True, verbose_name="Tiros a puerta"
    )  # fb_SoT
    perc_shoots_on_target = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de tiros a puerta"
    )  # fb_SoT_perc
    shoots_90 = models.FloatField(
        default=0, blank=True, verbose_name="Tiros por 90 minutos"
    )  # fb_Sh_90
    shoots_on_target_90 = models.FloatField(
        default=0, blank=True, verbose_name="Tiros a puerta por 90 minutos"
    )  # fb_SoT_90
    goals_per_shoot = models.FloatField(
        default=0, blank=True, verbose_name="Goles por tiro"
    )  # fb_G_vs_Sh
    goals_per_shoot_on_target = models.FloatField(
        default=0, blank=True, verbose_name="Goles por tiro a puerta"
    )  # fb_G_vs_SoT
    mean_distance_from_goals_shoots = models.FloatField(
        default=0, blank=True, verbose_name="Distancia media de los goles"
    )  # fb_Dist
    free_kicks_shooted = models.IntegerField(
        default=0, blank=True, verbose_name="Faltas lanzadas"
    )  # fb_FK
    npxg_per_shoot = models.FloatField(
        default=0, blank=True, verbose_name="npxG por tiro"
    )  # fb_npxG_vs_Sh
    goals_minus_expected_goals = models.FloatField(
        default=0, blank=True, verbose_name="Goles menos coles esperados"
    )  # fb_G_minus_xG
    passes_completed = models.IntegerField(
        default=0, blank=True, verbose_name="Pases completados"
    )  # fb_passes_Cmp
    passes_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Pases intentados"
    )  # fb_passes_Att
    perc_passes = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de pases completados"
    )  # fb_passes_Cmp_perc
    total_distance_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Distancia total en pases"
    )  # fb_passes_TotDist
    total_distance_progressive_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Distancia total en pases progresivos"
    )  # fb_passes_PrgDist
    short_passes_completed = models.IntegerField(
        default=0, blank=True, verbose_name="Pases cortos completados"
    )  # fb_passes_Short_Cmp
    short_passes_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Pases cortos intentados"
    )  # fb_passes_Short_Att
    perc_short_passes = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de pases cortos completados"
    )  # fb_passes_Short_Cmp_perc
    medium_passes_completed = models.IntegerField(
        default=0, blank=True, verbose_name="Pases medios completados"
    )  # fb_passes_Medium_Cmp
    medium_passes_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Pases medios intentados"
    )  # fb_passes_Medium_Att
    perc_medium_passes = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de pases medios completados"
    )  # fb_passes_Medium_Cmp_perc
    long_passes_completed = models.IntegerField(
        default=0, blank=True, verbose_name="Pases largos completados"
    )  # fb_passes_Long_Cmp
    long_passes_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Pases largos intentados"
    )  # fb_passes_Long_Att
    perc_long_passes = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de apses largos completados"
    )  # fb_passes_Long_Cmp_perc
    key_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases clave"
    )  # fb_key_passes
    last_third_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases al último tercio"
    )  # fb_last_third_passes
    ppa = models.IntegerField(
        default=0, blank=True, verbose_name="Pases completados al área (PPA)"
    )  # fb_PPA
    crosses_pa = models.IntegerField(
        default=0, blank=True, verbose_name="Centros completados al área"
    )  # fb_CrsPA
    progresive_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases progresivos completados"
    )  # fb_progresive_passes
    progresive_passes_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Pases prograsivos intentados"
    )  # fb_progresive_passes_Att
    live_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases en juego"
    )  # fb_Pass_Types_Live
    dead_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases desde juego parado"
    )  # fb_Pass_Types_Dead
    free_kick_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases de falta"
    )  # fb_Pass_Types_FK
    to_back_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases al espacio"
    )  # fb_Pass_Types_TB
    pressed_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases bajo presión de rival"
    )  # fb_Pass_Types_Press
    swap_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Cambios de juego horizontal"
    )  # fb_Pass_Types_Sw
    crosses = models.IntegerField(
        default=0, blank=True, verbose_name="Centros"
    )  # fb_Pass_Types_Crs

    corner_kicks = models.IntegerField(
        default=0, blank=True, verbose_name="Lanzamientos de corner"
    )  # fb_Pass_Types_CK
    corner_kicks_in = models.IntegerField(
        default=0, blank=True, verbose_name="Corners al área"
    )  # fb_Corner_Kicks_In
    corner_kicks_out = models.IntegerField(
        default=0, blank=True, verbose_name="Corners en corto"
    )  # fb_Corner_Kicks_Out
    corner_kicks_straight = models.IntegerField(
        default=0, blank=True, verbose_name="Corners directos"
    )  # fb_Corner_Kicks_Str

    ground_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases rasos"
    )  # fb_Height_Ground
    low_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases a baja altura"
    )  # fb_Height_Low
    high_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases por alto"
    )  # fb_Height_High

    left_foot_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases con la izquierda"
    )  # fb_Body_Parts_Left
    right_foot_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases con la derecha"
    )  # fb_Body_Parts_Right
    head_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases con la cabeza"
    )  # fb_Body_Parts_Head
    throw_in_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Saques de banda"
    )  # fb_Body_Parts_TI
    other_body_parts_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases con otras partes del cuerpo"
    )  # fb_Body_Parts_Other

    offsides_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases que son fuera de juego"
    )  # fb_Outcomes_Offsides
    out_off_bound_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases que salen fuera"
    )  # fb_Outcomes_Out
    intercepted_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases que son interceptados"
    )  # fb_Outcomes_Int
    blocked_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases que son bloqueados"
    )  # fb_Outcomes_Blocks

    sca = models.IntegerField(
        default=0, blank=True, verbose_name="Acciones que crean tiro"
    )  # fb_SCA_SCA
    sca_90 = models.FloatField(
        default=0, blank=True, verbose_name="Acciones que crean tiro por 90 minutos"
    )  # fb_SCA_SCA90
    sca_live_pass = models.IntegerField(
        default=0, blank=True, verbose_name="SCA desde pases en juego"
    )  # fb_SCA_Types_PassLive
    sca_dead_pass = models.IntegerField(
        default=0, blank=True, verbose_name="SCA desde juego parado"
    )  # fb_SCA_Types_PassDead
    sca_dribbling = models.IntegerField(
        default=0, blank=True, verbose_name="SCA desde regate"
    )  # fb_SCA_Types_Drib
    sca_another_shoot = models.IntegerField(
        default=0, blank=True, verbose_name="SCA desde otro tiro"
    )  # fb_SCA_Types_Sh
    sca_foul_drawn = models.IntegerField(
        default=0, blank=True, verbose_name="SCA desde falta provocada"
    )  # fb_SCA_Types_Fld
    sca_defensive_action = models.IntegerField(
        default=0, blank=True, verbose_name="SCA desde acción defensiva"
    )  # fb_SCA_Types_Def

    gca = models.IntegerField(
        default=0, blank=True, verbose_name="Acciones que crean gol"
    )  # fb_GCA_GCA
    gca_90 = models.FloatField(
        default=0, blank=True, verbose_name="Acciones que crean gol por 90 minutos"
    )  # fb_GCA_GCA90
    gca_live_pass = models.IntegerField(
        default=0, blank=True, verbose_name="GCA desde pases en juego"
    )  # fb_GCA_Types_PassLive
    gca_dead_pass = models.IntegerField(
        default=0, blank=True, verbose_name="GCA desde juego parado"
    )  # fb_GCA_Types_PassDead
    gca_dribbling = models.IntegerField(
        default=0, blank=True, verbose_name="GCA desde regate"
    )  # fb_GCA_Types_Drib
    gca_another_shoot = models.IntegerField(
        default=0, blank=True, verbose_name="GCA desde otro tiro"
    )  # fb_GCA_Types_Sh
    gca_foul_drawn = models.IntegerField(
        default=0, blank=True, verbose_name="GCA desde falta provocada"
    )  # fb_GCA_Types_Fld
    gca_defensive_action = models.IntegerField(
        default=0, blank=True, verbose_name="GCA desde acción defensiva"
    )  # fb_GCA_Types_Def

    # ACCIONES DEFENSIVAS
    tackles = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas"
    )  # fb_Tackles_Tkl
    tackles_wins = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas ganadas"
    )  # fb_Tackles_TklW
    tackles_def_third = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas en tercio defensivo"
    )  # fb_Tackles_Def_3rd
    tackles_mid_third = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas en tercio medio"
    )  # fb_Tackles_Mid_3rd
    tackles_att_third = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas en tercio atacante"
    )  # fb_Tackles_Att_3rd
    tackles_vs_dribbles_wins = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas ganadas contra regates"
    )  # fb_vs_Dribbles_Tkl
    tackles_vs_dribbles_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas contra regates"
    )  # fb_vs_Dribbles_Att
    perc_tackles_vs_dribbles = models.FloatField(
        default=0,
        blank=True,
        verbose_name="Porcentaje de entradas ganadas contra regates",
    )  # fb_vs_Dribbles_Tkl_perc
    pressures = models.IntegerField(
        default=0, blank=True, verbose_name="Presiones"
    )  # fb_Pressures_Press
    pressures_success = models.IntegerField(
        default=0, blank=True, verbose_name="Presiones exitosas"
    )  # fb_Pressures_Succ
    perc_pressures_success = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de presiones exitosas"
    )  # fb_Pressures_perc
    pressures_def_third = models.IntegerField(
        default=0, blank=True, verbose_name="Presiones en tercio defensivo"
    )  # fb_Pressures_Def_3rd
    pressures_mid_third = models.IntegerField(
        default=0, blank=True, verbose_name="Presiones en tercio medio"
    )  # fb_Pressures_Mid_3rd
    pressures_att_third = models.IntegerField(
        default=0, blank=True, verbose_name="Presiones en tercio atacante"
    )  # fb_Pressures_Att_3rd
    blocks = models.IntegerField(
        default=0, blank=True, verbose_name="Bloqueos"
    )  # fb_Blocks
    blocks_shoots = models.IntegerField(
        default=0, blank=True, verbose_name="Tiros bloqueados"
    )  # fb_Blocks_Sh
    blocks_shoots_on_target = models.IntegerField(
        default=0, blank=True, verbose_name="Tiros a puerta bloqueados"
    )  # fb_Blocks_ShSv
    blocks_passes = models.IntegerField(
        default=0, blank=True, verbose_name="Pases bloqueados"
    )  # fb_Blocks_Pass
    interceptions = models.IntegerField(
        default=0, blank=True, verbose_name="Intercepciones"
    )  # fb_Interceptions
    tackles_plus_interceptions = models.IntegerField(
        default=0, blank=True, verbose_name="Entradas mas intercepciones"
    )  # fb_Tkl_plus_Int
    clearances = models.IntegerField(
        default=0, blank=True, verbose_name="Despejes"
    )  # fb_Clearances
    errors_to_rival_shoot = models.IntegerField(
        default=0, blank=True, verbose_name="Errores que provocan tiro rival"
    )  # fb_Errors
    aerial_duels_won = models.IntegerField(
        default=0, blank=True, verbose_name="Duelos aéreos ganados"
    )  # fb_Aerial_Duels_Won
    aerial_duels_lost = models.IntegerField(
        default=0, blank=True, verbose_name="Duelos aéreos perdidos"
    )  # fb_Aerial_Duels_Lost
    perc_aerial_duels_won = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de duelos aéreos ganados"
    )  # fb_Aerial_Duels_Won_perc

    # ACCIONES DE JUEGO DE ATAQUE
    touches = models.IntegerField(
        default=0, blank=True, verbose_name="Toques"
    )  # fb_Touches
    touches_def_box = models.IntegerField(
        default=0, blank=True, verbose_name="Toques en área propia"
    )  # fb_Touches_Def_Pen
    touches_def_third = models.IntegerField(
        default=0, blank=True, verbose_name="Toques en tercio defensivo"
    )  # fb_Touches_Def_3rd
    touches_mid_third = models.IntegerField(
        default=0, blank=True, verbose_name="Toques en tercio medio"
    )  # fb_Touches_Mid_3rd
    touches_att_third = models.IntegerField(
        default=0, blank=True, verbose_name="Toques en tercio atacante"
    )  # fb_Touches_Att_3rd
    touches_att_box = models.IntegerField(
        default=0, blank=True, verbose_name="Toques en área rival"
    )  # fb_Touches_Att_Pen
    dribbles_success = models.IntegerField(
        default=0, blank=True, verbose_name="Regates exitosos"
    )  # fb_Dribbles_Succ
    dribbles_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Regates intentados"
    )  # fb_Dribbles_Att
    perc_dribbles_success = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de regates exitosos"
    )  # fb_Dribbles_Succ_perc
    number_players_dribbled = models.IntegerField(
        default=0, blank=True, verbose_name="Jugadores regateados"
    )  # fb_Dribbles_number_Pl
    dribbles_megs = models.IntegerField(
        default=0, blank=True, verbose_name="Regates con caño"
    )  # fb_Dribbles_Megs
    carries = models.IntegerField(
        default=0, blank=True, verbose_name="Conducciones"
    )  # fb_Carries
    distance_carries = models.IntegerField(
        default=0, blank=True, verbose_name="Distancia en conducción"
    )  # fb_Carries_TotDist
    progressive_distance_carries = models.IntegerField(
        default=0, blank=True, verbose_name="Distancia en conducciones progresivas"
    )  # fb_Carries_PrgDist
    progressive_carries = models.IntegerField(
        default=0, blank=True, verbose_name="Conducciones progresivas"
    )  # fb_Carries_Prog
    carries_last_third = models.IntegerField(
        default=0, blank=True, verbose_name="Conducciones hasta el tercio atacante"
    )  # fb_Carries_last_third
    carries_to_att_box = models.IntegerField(
        default=0, blank=True, verbose_name="Conducciones hasta área rival"
    )  # fb_Carries_CPA
    carries_missed = models.IntegerField(
        default=0, blank=True, verbose_name="Conducciones con pérdida por mal control"
    )  # fb_Carries_Mis
    carries_intercepted = models.IntegerField(
        default=0, blank=True, verbose_name="Conducciones con pérdida por robo rival"
    )  # fb_Carries_Dis
    receiving_target = models.IntegerField(
        default=0, blank=True, verbose_name="Objetivo de pases"
    )  # fb_Receiving_Targ
    receiving_target_success = models.IntegerField(
        default=0, blank=True, verbose_name="Objetivo de pases con éxito"
    )  # fb_Receiving_Rec
    perc_receiving_target_success = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de objetivo de pases con éxito"
    )  # fb_Receiving_Rec_perc
    receiving_target_progressive = models.IntegerField(
        default=0, blank=True, verbose_name="Objetivo de pases progresivos"
    )  # fb_Receiving_Prog

    yellow_cards = models.IntegerField(
        default=0, blank=True, verbose_name="Tarjetas amarillas"
    )  # fb_CrdY
    red_cards = models.IntegerField(
        default=0, blank=True, verbose_name="Tarjetas rojas"
    )  # fb_CrdR
    double_yellow_cards = models.IntegerField(
        default=0, blank=True, verbose_name="Dobles tarjetas amarillas"
    )  # fb_Performance_2CrdY
    fouls = models.IntegerField(
        default=0, blank=True, verbose_name="Faltas"
    )  # fb_Performance_Fouls
    fouls_drawn = models.IntegerField(
        default=0, blank=True, verbose_name="Faltas provocadas"
    )  # fb_Performance_Fouls_drawn
    offsides = models.IntegerField(
        default=0, blank=True, verbose_name="Fueras de juego"
    )  # fb_Performance_Offsides
    penalties_wons = models.IntegerField(
        default=0, blank=True, verbose_name="Penatis provocados"
    )  # fb_Performance_PKwon
    penalties_conceded = models.IntegerField(
        default=0, blank=True, verbose_name="Penaltis cometidos"
    )  # fb_Performance_PKconceded
    own_goals = models.IntegerField(
        default=0, blank=True, verbose_name="Goles en propia puerta"
    )  # fb_Performance_OG
    recoveries = models.IntegerField(
        default=0, blank=True, verbose_name="Recuperaciones"
    )  # fb_Performance_Recov

    class Meta:
        """Meta definition for PlayerStats."""

        verbose_name = "Estadísticas del jugador"
        verbose_name_plural = "Estadísticas de los jugadores"

    def __str__(self):
        """Unicode representation of PlayerStats."""
        return "Estadísticas de {} (Temp. {})".format(self.player, self.season)

    def save(self):
        """Save method for PlayerStats."""
        pass

    def get_absolute_url(self):
        """Return absolute url for PlayerStats."""
        return ""


""" TODO Añadir estos campos con cariño para una pantalla especial sólo de "Aportación al equipo"
    fb_Team_Success_PPM = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_PPM
    fb_Team_Success_onG = models.IntegerField(
        default=0, blank=True
    )  # fb_Team_Success_onG
    fb_Team_Success_onGA = models.IntegerField(
        default=0, blank=True
    )  # fb_Team_Success_onGA
    fb_Team_Success_dif = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_dif
    fb_Team_Success_dif_90 = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_dif_90
    fb_Team_Success_On_Off = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_On_Off
    fb_Team_Success_xG_onxG = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_xG_onxG
    fb_Team_Success_xG_onxGA = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_xG_onxGA
    fb_Team_Success_xG_xGdif = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_xG_xGdif
    fb_Team_Success_xG_xGdif_90 = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_xG_xGdif_90
    fb_Team_Success_xG_On_Off = models.FloatField(
        default=0, blank=True
    )  # fb_Team_Success_xG_On_Off """


class GoalkeeperStats(models.Model):
    """Model definition for GoalkeeperStats."""

    id = models.UUIDField(editable=False, default=uuid.uuid4, primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Jugador")
    extraction_date = models.DateField(verbose_name="Fecha de extracción")
    season = models.CharField(max_length=30, verbose_name="Temporada")  # fb_season
    team = models.CharField(max_length=50, blank=True, verbose_name="Equipo")  # fb_team
    team_date_joined = models.DateField(
        blank=True, null=True, verbose_name="Fecha de inicio de contrato"
    )  # tm_date_joined
    team_contract_expires = models.DateField(
        blank=True, null=True, verbose_name="Fecha de fin de contrato"
    )  # tm_contract_expires
    competition = models.CharField(max_length=50, verbose_name="Competición")  # fb_comp
    ca_salary = models.DecimalField(max_digits=12, decimal_places=2)  # ca_salary
    tm_current_value = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # tm_current_value
    matches_played = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos jugados"
    )  # fb_playing_time_MP
    matches_starts = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos titular"
    )  # fb_playing_time_starts
    minutes_played = models.IntegerField(
        default=0, blank=True, verbose_name="Minutos jugados"
    )  # fb_playing_time_min
    minutes_per_match = models.IntegerField(
        default=0, blank=True, verbose_name="Minutos por partido"
    )  # fb_Playing_Time_Mn_vs_MP
    perc_minutes_played = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de minutos jugados"
    )  # fb_Playing_Time_Min_perc
    complete_matches_played = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos completos"
    )  # fb_Starts_Compl
    matches_as_substitute = models.IntegerField(
        default=0, blank=True, verbose_name="Partidos jugados como suplente"
    )  # fb_Subs_Subs
    mean_minutes_starts = models.IntegerField(
        default=0, blank=True, verbose_name="Media de minutos cuando es titular"
    )  # fb_Starts_Min_vs_Start
    mean_minutes_substitute = models.IntegerField(
        default=0, blank=True, verbose_name="Media de minutos cuando es suplente"
    )  # fb_Subs_Mn_vs_Sub
    playing_time_90s = models.FloatField(
        default=0, blank=True, verbose_name="Minutos entre 90"
    )  # fb_playing_time_90s
    assists = models.IntegerField(
        default=0, blank=True, verbose_name="Asistencias"
    )  # fb_Ast
    expected_assists = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias esperadas"
    )  # fb_xA
    assists_90 = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias por 90 minutos"
    )  # fb_Ast_90
    expected_assists_90 = models.FloatField(
        default=0, blank=True, verbose_name="Asistencias esperadas por 90 minutos"
    )  # fb_xA_90
    # ESTADISTICAS DE PORTERO
    goals_against = models.IntegerField(
        default=0, blank=True, verbose_name="Goles en contra"
    )  # fb_GA
    goals_against_90 = models.FloatField(
        default=0, blank=True, verbose_name="Goles en contra por 90 minutos"
    )  # fb_GA_90
    shoots_on_target_against = models.IntegerField(
        default=0, blank=True, verbose_name="Tiros a puerta en contra"
    )  # fb_SoTA
    saves = models.IntegerField(
        default=0, blank=True, verbose_name="Paradas"
    )  # fb_saves
    perc_saves = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de paradas"
    )  # fb_save_perc
    clear_scores = models.IntegerField(
        default=0, blank=True, verbose_name="Porterias a cero"
    )  # fb_CS
    perc_clear_scores = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de porterias a cero"
    )  # fb_CS_perc
    penalty_against = models.IntegerField(
        default=0, blank=True, verbose_name="Penaltis en contra"
    )  # fb_PK_against
    penalty_saves = models.IntegerField(
        default=0, blank=True, verbose_name="Penaltis parados"
    )  # fb_PK_saves
    perc_penalty_saves = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de penaltis parados"
    )  # fb_PK_saves_perc
    psxg = models.FloatField(default=0, blank=True, verbose_name="PSxG")  # fb_PSxG
    psxg_per_shoots = models.FloatField(
        default=0, blank=True, verbose_name="PSxG por tiro a puerta"
    )  # fb_PSxG_vs_SoT
    psxg_diference = models.FloatField(
        default=0, blank=True, verbose_name="Diferencia de PSxG"
    )  # fb_PSxG_dif
    launches_completed = models.IntegerField(
        default=0, blank=True, verbose_name="Lanzamuentos completados"
    )  # fb_Launched_Cmp
    launches_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Lanzamientos realizados"
    )  # fb_Launched_Att
    perc_launches_completed = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de lanzamientos intentados"
    )  # fb_Launched_Cmp_perc
    passes_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Pases realizados"
    )  # fb_Passes_Att
    average_lenght_passes = models.FloatField(
        default=0, blank=True, verbose_name="Distancia media de los pases"
    )  # fb_Passes_AvgLen
    goal_kicks_attempted = models.IntegerField(
        default=0, blank=True, verbose_name="Saques de puerta realizados"
    )  # fb_Goal_Kicks_Att
    perc_goal_kicks_completed = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de saques de puerta completados"
    )  # fb_Goal_Kicks_Launch_perc
    average_lenght_goal_kick = models.FloatField(
        default=0, blank=True, verbose_name="Distancia media de los saques de puerta"
    )  # fb_Goal_Kicks_AvgLen
    opponent_crosses = models.IntegerField(
        default=0, blank=True, verbose_name="Centros del rival"
    )  # fb_Crosses_Opp
    opponent_crosses_stopped = models.IntegerField(
        default=0, blank=True, verbose_name="Centros del rival parados"
    )  # fb_Crosses_Stp
    perc_opponent_crosses_stopped = models.FloatField(
        default=0, blank=True, verbose_name="Porcentaje de centros del rival parados"
    )  # fb_Crosses_Stp_perc
    sweeper_opa = models.FloatField(
        default=0, blank=True, verbose_name="Salidas del área"
    )  # fb_Sweeper_OPA
    sweeper_opa_90 = models.FloatField(
        default=0, blank=True, verbose_name="Salidas del área por 90 minutos"
    )  # fb_Sweeper_OPA_90
    average_distance_sweeper = models.FloatField(
        default=0, blank=True, verbose_name="Distancia media de las salidas del área"
    )  # fb_Sweeper_AvgDist
    yellow_cards = models.IntegerField(
        default=0, blank=True, verbose_name="Tarjetas amarillas"
    )  # fb_CrdY
    red_cards = models.IntegerField(
        default=0, blank=True, verbose_name="Tarjetas rojas"
    )  # fb_CrdR

    class Meta:
        """Meta definition for GoalkeeperStats."""

        verbose_name = "Estadísticas del portero"
        verbose_name_plural = "Estadísticas de los porteros"

    def __str__(self):
        """Unicode representation of GoalkeeperStats."""
        return "Estadísticas de {} - (Temp. {})".format(self.player, self.season)

    def save(self):
        """Save method for GoalkeeperStats."""
        pass

    def get_absolute_url(self):
        """Return absolute url for GoalkeeperStats."""
        return ""


class Scoring(models.Model):
    """Model definition for Scoring."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    player = models.ForeignKey(
        Player, blank=False, on_delete=models.CASCADE, verbose_name="Jugador"
    )
    scoring = models.FloatField(blank=False, verbose_name="Scoring")
    calculate_date = models.DateTimeField(
        auto_now_add=True, blank=False, verbose_name="Fecha del cálculo"
    )
    index_used = models.ForeignKey(
        Index, on_delete=models.RESTRICT, verbose_name="Index usado"
    )
    active = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Scoring."""

        verbose_name = "Scoring"
        verbose_name_plural = "Scorings"

    def __str__(self):
        """Unicode representation of Scoring."""
        return "{} - ({})".format(self.player, self.scoring)

    def save(self):
        """Save method for Scoring."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Scoring."""
        return ""
