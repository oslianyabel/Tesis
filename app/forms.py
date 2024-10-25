# app/forms.py
from django import forms

class OpinionForm(forms.Form):
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'comentario', 'rows': 4}),
        required=False,
        label='Comentario'
    )

    puntuacion_choices = [(str(i), f"{i} Estrellas") for i in range(1, 6)]
    puntuacion = forms.ChoiceField(
        choices=puntuacion_choices,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'puntuacion'}),
        required=True,
        label='Puntuación'
    )
