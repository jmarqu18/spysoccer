import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone


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
        """Save method for Index."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Scoring."""
        return ""
