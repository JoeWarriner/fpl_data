from django import forms
from apps.predictor.models import Player

class PositionSelecter(forms.ModelForm):
    
    class Meta:
        model = Player
        fields = ['position']