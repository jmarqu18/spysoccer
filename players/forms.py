from django import forms

from .models import ScoringRequest, SimilarityRequest


class CalculateScoringForm(forms.ModelForm):
    class Meta:
        model = ScoringRequest
        exclude = [
            "user",
        ]


class CalculateSimilarityForm(forms.ModelForm):
    class Meta:
        model = SimilarityRequest
        exclude = [
            "user",
        ]
