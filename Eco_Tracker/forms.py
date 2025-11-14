from django import forms

class CarUsageForm(forms.Form):
    manejó_auto = forms.ChoiceField(
        choices=[('yes', 'Sí'), ('no', 'No')], 
        label="¿Manejaste un auto hoy?",
        widget=forms.RadioSelect
    )
    tipo_auto = forms.CharField(
        max_length=100, 
        required=False, 
        label="Tipo de auto (ej: Sedan, SUV, Hatchback)"
    )
    distancia = forms.FloatField(
        label="Distancia recorrida (km)",
        required=False
    )
    tiempo = forms.FloatField(
        label="Tiempo manejando (horas)",
        required=False
    )