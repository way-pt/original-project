from django import forms
from django.forms import ModelForm

from core.models import Map

class NewMapForm(ModelForm):

    class Meta:
        model = Map
        fields = ['name', 'data']
