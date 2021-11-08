from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, UserLoginForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages


def home_view(request):
    return render(request, 'index.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            group_name = form.cleaned_data.get('group')
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            # user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = RegisterForm()
    return render(request, './account/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        # user = User.objects.get(username=request.POST['username'])
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
        # user = form.login(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
            # return render(request, './account/success.html')
        else:
            messages.error(request, "Erreur d'authentification ! Merci de réessayer.")
            return redirect('login')
    else:
        form = UserLoginForm()
    return render(request, './account/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def login_success(request):
    return render(request, './account/success.html')