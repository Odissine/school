from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .core import generate_username, generate_email


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre prénom'}, label='', widget=forms.TextInput(attrs={'placeholder': 'Prénom'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre nom de famille'}, label='', widget=forms.TextInput(attrs={'placeholder': 'Nom'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='', required=True, error_messages={'required': 'Merci de choisir votre classe'}, empty_label='Classe')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'}), label='')

    def save(self, commit=True):
        instance = super(RegisterForm, self).save(commit=False)
        instance.username = generate_username(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        instance.email = generate_email(instance.username, 'endtg.com')
        if commit:
            instance.save()

        return instance

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'group', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", 'autofocus': 'None'}), label="", required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}), label='')
    username.widget.attrs.update({"autofocus": False})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Désolé, cet identifiant n'existe pas ! Essaye encore ... ou créé toi un compte :)")
        return self.cleaned_data
