from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .core import generate_username, generate_email


class RegisterForm(UserCreationForm):

    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    def save(self, commit=True):
        instance = super(RegisterForm, self).save(commit=False)
        instance.username = generate_username(self.cleaned_data['first_name'], self.cleaned_data['last_name'])
        instance.email = generate_email(instance.username, 'endtg.com')
        if commit:
            print(instance)

            # instance.save()

        # group_choose = Group.objects.get(name='group')
        # group_choose.user_set.add(instance)

        return instance

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'group', 'password1', 'password2')
