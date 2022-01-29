from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, UserLoginForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .core import get_moyenne_score, get_max_score


class MyChangeFormPassword(PasswordChangeForm):
    pass


def group_required(*group_names):

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


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
            return redirect('account:login')
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
        user = User.objects.get(pk=request.POST['username'])
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
        # user = form.login(request)
        # username = request.POST['username']
        username = user.username

        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
            # return render(request, './account/success.html')
        else:
            messages.warning(request, "Erreur d'authentification ! Merci de réessayer.")
            return redirect('account:login')

    return render(request, './account/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('account:login')


@login_required
def login_success(request):
    return render(request, './account/success.html')


@login_required
@group_required('ADMIN')
def user_list(request):
    if request.method == "POST":
        group = request.POST['group']
    else:
        group = None
    if group:
        group_name = group
        users = User.objects.filter(groups__name=group)
    else:
        group_name = "TOUS LES GROUPES"
        users = User.objects.all()
    list = []
    for user in users:
        classe = user.groups.first()
        moyenne_mot = get_moyenne_score(user, 'mot')
        moyenne_lettre = get_moyenne_score(user, 'lettre')
        max_mot = get_max_score(user, 'mot')
        max_lettre = get_max_score(user, 'lettre')

        list.append({
            'id': user.id,
            'prenom': user.first_name,
            'nom': user.last_name,
            'classe': classe.name,
            'username': user.username,
            'moyenne_mot': moyenne_mot,
            'moyenne_lettre': moyenne_lettre,
            'max_mot': max_mot,
            'max_lettre': max_lettre,
        })

    context = {'list': list, 'group_name': group_name}
    return render(request, './account/list.html', context)
    

# def password_reset(self, request):
#     instance_user = get_object_or_404(User, id=int(user_id))
#     form_edit_password = MyChangeFormPassword(instance_user)
#     context={'form_edit_password': form_edit_password}
# 
#    return render(request, './account/password.html', context)