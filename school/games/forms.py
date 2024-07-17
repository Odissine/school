from django.forms import ModelForm
from .models import Halo, WordOne, Group
from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from django.core.validators import MaxLengthValidator


class WordFormOneList(forms.Form):

    LEVEL_CHOICES = (
        ("", ""),
        ("1", "Niveau 1"),
        ("2", "Niveau 2"),
        ("3", "Niveau 3"),
    )
    mots = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=True)
    group = forms.ModelMultipleChoiceField(
        widget=Select2MultipleWidget(attrs={'placeholder': 'Groupe', 'class': 'form-control'}),
        queryset=Group.objects.all(),
        required=True)
    level = forms.ChoiceField(widget=Select2Widget, choices=LEVEL_CHOICES, required=False)

    class Meta:
        model = WordOne
        fields = ('mots', 'group', 'level')


class HaloForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput, required=False)
    url = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Halo
        fields = ('name', 'image', 'url')
