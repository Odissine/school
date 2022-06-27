from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, UserLoginForm, UserProfil, SupportForm
from django.contrib.auth.models import Group, User
from django.db.models import Max
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.apps import apps
from .core import get_moyenne_score, get_max_score, generate_random_token, send_mail, verify_mail_gmass
from django.core import serializers
from django.http import HttpResponse
from .models import TokenLogin, Player
from school.settings import DEBUG
from django.utils.html import format_html

from io import BytesIO
import xlsxwriter
import pandas as pd
# from games.models import *
import logging
logger = logging.getLogger(__name__)


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


def support_view(request):
    form = SupportForm(request.POST or None)
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            messages.success(request, "Message envoyé !")
            return redirect('account:support')
    context = {
        'form': form,
    }
    return render(request, './account/support.html', context)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.get_username()
            try:
                user = User.objects.get(username=username)
                messages.error(request, "Compte déjà existant : <b>" + str(username) + "</b> ! Merci de réessayer.")
                return redirect('account:register')
            except:
                if verify_mail_gmass(username+"@endtg.com") is False:
                    messages.error(request, "Vous devez d'abord avoir une adresse mail de l'établissement ! Veuillez contacter le support informatique (support@endtg.com).")
                    return redirect('account:register')
                user = form.save()
                group_name = form.cleaned_data.get('group')
                group = Group.objects.get(name=group_name)
                user.groups.add(group)

                Player.objects.create(user=user, confirm=False)

                if DEBUG is True:
                    href = "http://127.0.0.1:8000/account/validation"
                    # href = "https://endtg.pythonanywhere.com/account/validation"
                else:
                    href = "https://endtg.pythonanywhere.com/account/validation"

                email_html = "<br/><br/>Bonjour " + user.first_name + ",<br/><br/>"
                email_html += "Vous venez de créer un compte sur le site <a href='http://endtg.pythonanywhere.com'>School @ ENDTG</a><br>"
                email_html += "Cliquez sur le lien ci-dessous afin de valider votre inscription.<br/><br/>"
                email_html += "<a href='" + href + "'>Validation du compte</a><br/><br/>"
                email_html += "Si vous n'êtes pas à l'origine de cette demande, merci de bien vouloir trasnférer ce mail à l'adresse suivante : support@endtg.com.<br/><br/>"
                email_html += "Equipe Support - School @ ENDTG"
                print("User mail to user : ", user.email)
                #   send_mail("School @ ENDTG - Bienvenue !", email_html, '', '', user.email, '')

                # user = authenticate(username=username, password=password)
                # login(request, user)
                messages.success(request, "Compte créé avec succès ... Un mail de validation vous a été envoyé à l'adresse " + str(user.email) + ".")
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

        # user = User.objects.get(pk=request.POST['username'])
        # user.backend = 'django.contrib.auth.backends.ModelBackend'
        # user = form.login(request)
        username = request.POST['username']
        logger.info(str(username) + " tente de se connecter ...")
        # username = user.username
        password = request.POST['password']
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except:
                user = None
            # user = authenticate(request, email=username, password=password)
        else:
            try:
                user = User.objects.get(username=username)
            except:
                user = None
            user = authenticate(request, username=username, password=password)
        if user is not None and user.check_password(password):
            login(request, user)
            logger.info(str(username) + " s'est connecté(e)")
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
    quizScore = apps.get_model('poll', 'QuizInstance')
    quizModel = apps.get_model('poll', 'Quiz')

    dic_user = {}
    quizs = quizModel.objects.all()
    users = User.objects.all().order_by('last_name', 'first_name').distinct()
    for user in users:
        classe = ','.join(map(lambda x: str(x[0]), user.groups.all().values_list('name')))
        dic_user[user.id] = {'Prénom': user.first_name, 'Nom': user.last_name, 'Classe': classe}
        letter_scores = letterScore.objects.filter(user=user)
        word_scores = wordScore.objects.filter(user=user)
        max_level_letter = letterScore.objects.all().aggregate(Max('level'))
        max_level_word = wordScore.objects.all().aggregate(Max('level'))

        for level in range(1, int(max_level_letter['level__max']) + 1):
            try:
                score_letter = letterScore.objects.get(user=user, level=level)
                score_letter = score_letter.score
            except:
                score_letter = 0

            dic_user[user.id].update({'L'+str(level): score_letter})

        for level in range(1, int(max_level_word['level__max']) + 1):
            try:
                score_word = wordScore.objects.get(user=user, level=level)
                score_word = score_word.score
            except:
                score_word = 0
            dic_user[user.id].update({'M'+str(level): score_word})
        i = 1
        for quiz in quizs:
            try:
                quiz_score = quizScore.objects.get(player=user, quiz=quiz)
                quiz_score = quiz_score.score
            except:
                quiz_score = 0
            dic_user[user.id].update({'Q' + str(i): quiz_score})
            i += 1

    df = pd.DataFrame.from_dict(dic_user, orient='index')

    with BytesIO() as b:
        with pd.ExcelWriter(b) as writer:
            df.to_excel(writer, sheet_name='Users')

        filename = 'export_users.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
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


def help_view(request):
    context = {}
    return render(request, './account/help.html', context)


@login_required()
def pref_view(request):
    form = UserProfil(request.user, request.POST or None, instance=request.user, initial={'group': request.user.groups.first()})
    if request.POST:
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(pk=request.POST.get('group'))
            user.groups.clear()
            user.groups.add(group)
            message = "Profil modifié avec succès !"
            messages.success(request, message)
            return redirect('account:preferences')
        else:
            print(form.errors)
            message = "Une erreur s'est produit lors de la mise à jour !"
            messages.error(request, message)
            return redirect('account:preferences')
    context = {
        'form': form,
    }
    return render(request, './account/preferences.html', context)


@login_required()
def password_reset(request):
    if request.POST:
        password = request.POST.get("currentPassword")
        newpassword = request.POST.get("newPassword")
        confirmpassword = request.POST.get("renewPassword")
        if request.user.check_password(password):
            if newpassword == confirmpassword:
                request.user.set_password(password)
                request.user.save()
                message = "Mot de passe modifié avec succès !"
                messages.success(request, message)
                return redirect('account:preferences')
            else:
                message = "La confirmation du mot de passe ne correspond pas au mot de passe saisie !"
                messages.error(request, message)
                return redirect('account:preferences')
        else:
            message = "L'ancien mot de passe n'est le bon !"
            messages.error(request, message)
    context = {
    }
    return render(request, './account/preferences.html', context)


def lost_password(request):
    form = UserLoginForm(request.POST or None)
    user = None
    if request.method == "POST":
        username = request.POST['username']
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except:
                user = None
        else:
            try:
                user = User.objects.get(username=username)
            except:
                user = None
        if user is None:
            messages.error(request, "Un problème est survenu ... compte inexistant !")
            return redirect('account:forget')

        token_mail = generate_random_token(40)
        create_token = TokenLogin.objects.create(token=token_mail, user=user)

        if DEBUG is True:
            href = "http://127.0.0.1:8000/account/reset/" + str(user.id) + "/" + str(token_mail)
        else:
            href = "https://endtg.pythonanywhere.com/account/reset/" + str(user.id) + "/" + str(token_mail)

        email_html = "<br/><br/>Bonjour " + user.first_name + ",<br/><br/>"
        email_html += "Vous venez de faire une demande de réinitialisation de mot de passe sur le site <a href='http://endtg.pythonanywhere.com'>School @ ENDTG</a><br>"
        email_html += "Cliquez sur le lien ci-dessous afin de pouvoir changer votre mot de passe <br/><br/>"
        email_html += "<a href='" + href + "'>Changer son mot de passe</a><br/><br/>"
        email_html += "Si vous n'êtes pas à l'origine de cette demande, veuillez ne pas tenir compte de ce mail.<br/><br/>"
        email_html += "Equipe Support - School @ ENDTG"
        print("User mail to user : ", user.email)
        send_mail("School @ ENDTG - Mot de passe oublié", email_html, '', '', user.email, '')

        messages.success(request, "Un email vient de vous être envoyé !")
        return redirect("account:login")
        # user = authenticate(request, username=username, password=password)

    context = {
        'form': form,
    }
    return render(request, "account/forget.html", context)


def reset_password(request, user, token):
    try:
        user = User.objects.get(id=user)
    except:
        messages.error(request, "Vous n'êtes pas autorisé à modifier le mot de passe.")
        return redirect("account:login")

    try:
        token = TokenLogin.objects.get(user=user, token=token)
    except:
        messages.error(request, "Vous n'êtes pas autorisé à modifier le mot de passe.")
        return redirect("account:login")

    if request.POST:
        if request.POST.get('pass1') == request.POST.get('pass2') and request.POST.get('pass1') != "":
            user = request.POST.get('user')
            try:
                user = User.objects.get(id=user)
            except:
                messages.error(request, "Vous n'êtes pas autorisé à modifier le mot de passe.")
                return redirect("account:login")

            user.set_password(request.POST.get('pass1'))
            user.save()
            token.delete()

            if DEBUG is True:
                href = "http://127.0.0.1:8000/account/login"
                # href = "https://endtg.pythonanywhere.com/account/login"
            else:
                href = "https://endtg.pythonanywhere.com/account/login"

            email_html = "<br/><br/>Bonjour " + user.first_name + ",<br/><br/>"
            email_html += "Vous venez de modifier votre mot de passe pour accéder au site <a href='http://endtg.pythonanywhere.com'>School @ ENDTG</a><br>"
            email_html += "Cliquez sur le lien ci-dessous afin de pouvoir vous identifier.<br/><br/>"
            email_html += "<a href='" + href + "'>Identification</a><br/><br/>"
            email_html += "Si vous n'êtes pas à l'origine de cette demande, veuillez nous contacter afin que l'on puisse vous réinitialiser votre mot de passe.<br/><br/>"
            email_html += "Equipe Support - School @ ENDTG"
            print("User mail to user : ", user.email)
            send_mail("School @ ENDTG - Nouveau mot de passe", email_html, '', '', user.email, '')

            messages.success(request, format_html("Votre mot de passe a bien été réinitialisé."))
            return redirect("account:login")
        else:
            messages.error(request, format_html("Les mots de passe ne correspondent pas !<br> Veuillez réessayer."))
            return redirect('account:reset', user.id, token.token)

    context = {
        'user_reset': user,
        'token': token.token,
    }
    return render(request, "account/reset.html", context)
