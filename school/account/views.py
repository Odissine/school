from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegisterForm
from .core import generate_username, generate_email


def home_view(request):
    return render(request, 'index.html')


def register_view(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        group = form.cleaned_data.get('group')
        user = authenticate(username=username, password=password)
        print('Username : %s', username)
        print('User : %s', user)
        print('Group : %s', group)
        # login(request, user)
        return redirect('home')

    return render(request, './account/register.html', {'form': form})
