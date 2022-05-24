from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, UserLoginForm
from django.contrib.auth.models import Group, User
from django.db.models import Max
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.apps import apps
from .core import get_moyenne_score, get_max_score
from django.core import serializers
from django.http import HttpResponse

from io import BytesIO
import xlsxwriter

# from games.models import *


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
        return redirect('main:index-view')

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
            return redirect('main:index-view')
            # return render(request, './account/success.html')
        else:
            messages.error(request, "Erreur d'authentification ! Merci de réessayer.")
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
def user_list(request, order):
    order_criteria = "letterscore__score"
    if order == "ld":
        order_criteria = "-letterscore__score"
    if order == "la":
        order_criteria = "letterscore__score"
    if order == "wd":
        order_criteria = "-wordscore__score"
    if order == "wa":
        order_criteria = "wordscore__score"

    if request.method == "POST":
        group = request.POST['group']
    else:
        group = None
    if group:
        group_name = group
        users = User.objects.filter(groups__name=group).order_by(order_criteria, 'first_name').distinct()
    else:
        group_name = "TOUS LES GROUPES"
        users = User.objects.all().order_by(order_criteria, 'first_name').distinct()

    users_temp = []
    for user in users:
        if user not in users_temp:
            users_temp.append(user)
    users = users_temp

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

    context = {'list': list,
               'group_name': group_name,
               'order': order,
               }
    return render(request, './account/list.html', context)


@login_required
@group_required('ADMIN')
def export_user_excel(request):
    letterScore = apps.get_model('games', 'LetterScore')
    wordScore = apps.get_model('games', 'WordScore')

    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # EN-TETE

    # Create a format to use in the merged range.
    header_format = workbook.add_format({
        'bold': 1,
        'bottom': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'silver'
    })

    merge_format = workbook.add_format({
        'bold': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'silver',
    })

    cell_header_format = workbook.add_format({'bold': True, 'bg_color': 'green'})
    worksheet.set_column(3, 13, 10)
    worksheet.write(1, 0, 'NOM', header_format)
    worksheet.write(1, 1, 'PRENOM', header_format)
    worksheet.write(1, 2, 'CLASSE', header_format)
    worksheet.merge_range('D1:H1', 'LETTRES', merge_format)
    worksheet.write(1, 3, 'L1', header_format)
    worksheet.write(1, 4, 'L2', header_format)
    worksheet.write(1, 5, 'L3', header_format)
    worksheet.write(1, 6, 'L4', header_format)
    worksheet.write(1, 7, 'L5', header_format)
    worksheet.merge_range('I1:N1', 'MOTS', merge_format)
    worksheet.write(1, 8, 'L1', header_format)
    worksheet.write(1, 9, 'L2', header_format)
    worksheet.write(1, 10, 'L3', header_format)
    worksheet.write(1, 11, 'L4', header_format)
    worksheet.write(1, 12, 'L5', header_format)
    worksheet.write(1, 13, 'L6', header_format)

    if request.method == "POST":
        group = request.POST['group']
    else:
        group = None
    if group:
        group_name = group
        users = User.objects.filter(groups__name=group).order_by('last_name', 'first_name').distinct()
    else:
        group_name = "TOUS LES GROUPES"
        users = User.objects.all().order_by('last_name', 'first_name').distinct()

    users_temp = []
    for user in users:
        if user not in users_temp:
            users_temp.append(user)
    users = users_temp

    line = 2
    for user in users:
        classe = user.groups.first()
        worksheet.write(line, 0, user.first_name)
        worksheet.write(line, 1, user.last_name)
        worksheet.write(line, 2, classe.name)
        for level in range(1, 6):
            score = letterScore.objects.filter(user=user, level=level).first()
            if score is not None:
                score = score.score
            else:
                score = 0
            worksheet.write(line, level + 2, score)

        for level in range(1,7):
            score = wordScore.objects.filter(user=user, level=level).first()
            if score is not None:
                score = score.score
            else:
                score = 0
            worksheet.write(line, level + 7, score)
        line += 1

    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="export_eleves.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response


@login_required
@group_required('ADMIN')
def export_user_csv(request):
    letterScore = apps.get_model('games', 'LetterScore')
    wordScore = apps.get_model('games', 'WordScore')

    dic_user = {}
    users = User.objects.all().order_by('last_name', 'first_name').distinct()
    for user in users:
        dic_user[user.id] = {'Prénom': user.first_name, 'Nom': user.last_name, 'Classe': user.groups.name}
        letter_scores = letterScore.objects.filter(user=user)
        max_level_letter = letterScore.objects.all().aggregate(Max('level'))
        word_scores = wordScore.objects.filter(user=user)
        max_level_word = wordScore.objects.all().aggregate(Max('level'))
        print(max_level_letter)

        response = HttpResponse(serializers.serialize('json', users), content_type='application/json')

        return response

@login_required
@group_required('ADMIN')
def change_password(request):
    if request.method == "POST":
        id_user = request.POST['idUser']
        user = User.objects.filter(pk=id_user).first()
        user.set_password(request.POST['new_password'])
        user.save()
        message = "Mot de passe modifié avec succès pour ", user.first_name
        messages.success(request, message)

    return redirect('account:user-list', order='la')


@login_required()
@group_required('ADMIN', 'ENSEIGNANT')
def export_users(request):
    try:
        users = User.objects.all()
        response = HttpResponse(serializers.serialize('json', users), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="export_users.json"'
    except Exception:
        raise

    return response
