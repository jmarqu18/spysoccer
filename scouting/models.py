import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


from players.models import Player


def getUser():
    """La usamos para setear los reportes cuando
    es borrado el usuario que los hace, y no perderlos"""
    return get_user_model().objects.get_or_create(username="user_deleted")[0]


class PerformanceReport(models.Model):
    """Model definition for PerformanceReport."""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    scout = models.ForeignKey(
        get_user_model(), on_delete=models.SET(getUser), null=True, verbose_name="Scout"
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Jugador")
    creation_date = models.DateField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_date = models.DateField(auto_now=True, verbose_name="Última actualización")
    match_date = models.DateField(
        default=timezone.now, verbose_name="Fecha del partido visto"
    )
    notes = models.TextField(verbose_name="Notas del scout")
    # Métricas comunes
    height = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Talla/Altura",
    )
    physical_power = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Corpulencia/Fuerza",
    )
    right_foot = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Dominio de pie derecho",
    )
    left_foot = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Dominio de pie izquierdo",
    )
    determined = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Determinación/Agresividad",
    )
    intelligence = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Inteligencia",
    )
    # Métricas defensivas
    positioning = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Posicionamiento",
    )
    turns = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Giros/Cambios de dirección",
    )
    back_movement = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Carrera hacia atrás",
    )
    lateral_movement = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Movimiento lateral",
    )
    pace = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Ritmo/Velocidad",
    )
    quick_short_distance = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Velocidad en corta distancia",
    )
    covering_depth = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Cobertura de profundidad",
    )
    short_passing = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Pases cortos",
    )
    long_passing = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Pases largos",
    )
    traveling_ball = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Conducción de balón",
    )
    aerial_game = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Juego aéreo",
    )
    tackling = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Entradas",
    )
    anticipating = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Anticipación",
    )
    command_of_defence = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Mando sobre la defensa",
    )
    traveling_ball = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Conducción de balón",
    )
    composture_on_the_ball = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Serenidad con balón",
    )
    # Métricas ofensivas
    technique = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Técnica individual",
    )
    striking_ability = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Golpeo de balón/ABP",
    )
    vision = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Visión de juego",
    )
    key_passing = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Pases clave",
    )
    link_up_play = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Juego combinativo",
    )
    hold_up_play = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Aguantar el balón",
    )
    dynamism = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Dinamismo",
    )
    decision_making = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Toma de decisiones",
    )
    off_the_ball_movements = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Movimientos sin balón",
    )
    trickery = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Regates/Habilidad",
    )
    dealing_with_offside = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Control del fuera de juego",
    )
    work_rate = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Capacidad de trabajo",
    )
    shooting = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Disparo/Finalización",
    )
    through_passing = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Pases entre líneas",
    )
    coverings = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Cobertura",
    )
    defensive_capacity = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Capacidad defensiva",
    )
    box_to_box_ability = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Habilidad box to box",
    )
    build_up_capacity = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Capacidad creativa",
    )
    defensive_capacity = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Capacidad defensiva",
    )
    defensive_capacity = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Capacidad defensiva",
    )
    defensive_capacity = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Capacidad defensiva",
    )
    lateral_crosses = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Centros laterales",
    )
    arrival_baseline = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Llegada a línea de fondo",
    )
    gk_saves = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Paradas",
    )
    gk_footwork = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Juego con los pies",
    )
    gk_aerial_game = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Juego por alto/Salidas",
    )
    gk_penalty_saves = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Paradas de penalti",
    )
    gk_comunication = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Comunicación con la defensa",
    )
    gk_goal_kicks = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Saque de puerta",
    )
    gk_one_to_one = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Uno contra uno",
    )
    gk_box_domain = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Dominio del área",
    )
    gk_crosses = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Control de centros laterales",
    )
    gk_grip = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(5), MinValueValidator(0)],
        verbose_name="Agarre del balón",
    )

    class Meta:
        """Meta definition for PerformanceReport."""

        verbose_name = "Informe de rendimiento"
        verbose_name_plural = "Informes de rendimiento"

    def __str__(self):
        """Unicode representation of PerformanceReport."""
        return "{}".format(self.player)

    def save(self, *args, **kwargs):
        super(PerformanceReport, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for PerformanceReport."""
        return ""
