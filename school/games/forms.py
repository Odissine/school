from django.forms import ModelForm
from .models import Word, Halo
from django import forms


class WordForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = Word
        fields = ('name', 'level', 'image', 'group')


class HaloForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    url = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Halo
        fields = ('name', 'image', 'url')
