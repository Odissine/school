from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .core import generate_username, generate_email
from django_select2.forms import Select2Widget, ModelSelect2Widget, Select2MultipleWidget
from django.forms import ModelMultipleChoiceField, ModelChoiceField
from .models import *
from school.settings import IS_PRODUCTION


class UsernameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre prénom'}, label='',
                                 widget=forms.TextInput(attrs={'placeholder': 'Prénom', 'autocomplete': 'off'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre nom de famille'}, label='',
                                widget=forms.TextInput(attrs={'placeholder': 'Nom', 'autocomplete': 'off'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all().exclude(name__in=['ADMIN', 'ENSEIGNANT']), label='', required=True,
                                   error_messages={'required': 'Merci de choisir votre classe'}, empty_label='Classe',
                                   widget=Select2Widget(attrs={'placeholder': "Classe", 'class': 'js-example-basic-single form-control select'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmation du mot de passe'}), label='')

    def get_username(self):
        username = generate_username(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        return username

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


class UserLoginForm(forms.ModelForm):
    if IS_PRODUCTION is True:
        username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur ou adresse mail", 'autofocus': 'None'}),
                               label="", required=True)
    else:
        # username = forms.ModelChoiceField(widget=Select2Widget(attrs={'placeholder': "Nom d'utilisateur", 'class': 'form-control'}), queryset=User.objects.all(), label="Nom d'utilisateur", required=True, help_text="Merci d'indiquer votre nom d'utilisateur")
        username = UsernameChoiceField(label="Utilisateur", queryset=User.objects.all(), widget=Select2Widget(attrs={'placeholder': "Nom d'utilisateur", 'class': 'js-example-basic-single form-control select'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe', 'autocomplete': 'off'}),
                               label='Mot de passe')

    # username.widget.attrs.update({"autofocus": False})

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            raise forms.ValidationError("Désolé, cet identifiant n'existe pas ! Essaye encore ... ou créé toi un compte :)")
        else:
            confirm = Player.objects.get(user=user)
            if confirm.confirm is False:
                raise forms.ValidationError("Désolé, le compte n'est pas encore validé ! <a href=''>Renvoyer le mail de validation ?</a>")

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfil(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(UserProfil, self).__init__(*args, **kwargs)
        admin_group = Group.objects.get(name="ADMIN")
        if user.groups.first() == admin_group:
            self.fields['group'].queryset = Group.objects.all()
        else:
            self.fields['group'].queryset = Group.objects.exclude(name__in=["ADMIN", "ENSEIGNANT"])

    first_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre prénom'}, label='',
                                 widget=forms.TextInput(attrs={'placeholder': 'Prénom', 'autocomplete': 'off'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre nom de famille'}, label='',
                                widget=forms.TextInput(attrs={'placeholder': 'Nom', 'autocomplete': 'off'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='', required=True, error_messages={'required': 'Merci de choisir votre classe'},
                                   widget=Select2Widget(attrs={'class': 'js-example-basic-single form-control select', 'style': 'width:100%'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'group')


class SupportForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(SupportForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.exclude(name__in=["ADMIN", ])

    sujet = forms.CharField(required=True, error_messages={'required': 'Merci de saisir un sujet'}, label='',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet', 'autocomplete': 'off'}))
    message = forms.CharField(required=True, error_messages={'required': 'Merci de saisir un message'}, label='',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height:200px;', 'placeholder': 'Sujet', 'autocomplete': 'off'}))
    first_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre prénom'}, label='',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom', 'autocomplete': 'off'}))
    last_name = forms.CharField(required=True, error_messages={'required': 'Merci de saisir votre nom de famille'}, label='',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom', 'autocomplete': 'off'}))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='', required=False, error_messages={'required': 'Merci de choisir votre classe'},
                                   widget=Select2Widget(attrs={'class': 'js-example-basic-single form-control select', 'style': 'width:100%;'}))
