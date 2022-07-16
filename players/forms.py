from django import forms

from .models import Index, ScoringRequest

# Select para el estatus del scrape
SEASON_CHOICES = [
    ("2021-2022", "2021-2022"),
]


# class CalculateScoringForm(forms.Form):
#     index = forms.ModelChoiceField(
#         queryset=Index.objects.all(), label="Selecciona Index", required=True
#     )
#     season = forms.ChoiceField(choices=SEASON_CHOICES, required=True, label="Temporada")
#     minutes_played_min = forms.IntegerField(
#         required=True,
#         label="Mínimo de minutos jugados",
#         help_text="Jugadores que hayan jugado al menos estos minutos",
#     )
#     age = forms.IntegerField(
#         disabled=True,
#         label="Edad máxima",
#         help_text="Se implementará en futuras versiones",
#     )


class CalculateScoringForm(forms.ModelForm):
    class Meta:
        model = ScoringRequest
        exclude = [
            "user",
        ]
