import os
import urllib.request
import requests

from urllib.parse import urlparse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.text import slugify
from django.http import JsonResponse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile

from . import core
from .models import WordOne, WordScore, LetterScore, Halo, AdditionScore, MultiplicationScore, SoustractionScore, AdditionPoseeScore
from .forms import HaloForm, WordFormOneList
from school import settings
from .journal import *


def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups)


'''
UNE SOLUTION DE DECORATEUR DANS LA VUE

@user_passes_test(core.is_ce1)
def cp_view_bis(request, pk):
    return render(request, './games/word.html')
'''

'''
AUTRE SOLUTION DE DECORATEUR GROUP DANS LA VUE
@group_required('CP')
def cp_mots(request):
    return render(request, './games/word.html')
'''


# JEUX DE MOTS ----------------------------------------------------------------------------
@login_required()
def wordOne(request):
    # Filtre par Niveau
    if request.GET.get('l', ''):
        level = request.GET.get('l', '')
    else:
        level = "1"

    user = request.user
    wordScore = WordScore.objects.filter(user=user, level=level).first()
    if int(level) < 4:
        filterLevel = level
    else:
        filterLevel = int(level) - 3

    wordList = WordOne.objects.filter(level=filterLevel)
    wordListFormatted = []
    for elem in wordList:
        if int(level) < 4:
            wordListFormatted.append(str(elem.name.lower()))
        else:
            wordListFormatted.append(str(elem.name.capitalize()))
    wordListFormatted = json.dumps(wordListFormatted)

    if not wordScore:
        wordScore = 0
    else:
        wordScore = wordScore.score

    context_header = {'title': 'Mots'}

    context = {'level': level,
               'wordOneScore': wordScore,
               'word_list': wordListFormatted,
               'context_header': context_header,
               }
    return render(request, './games/word_one.html', context)


@login_required()
def saveWordOneProgress(request):
    level = request.POST.get("level")
    count = request.POST.get("score")
    user = request.user
    score = WordScore.objects.filter(level=level, user=user).first()
    if not score:
        instance = WordScore.objects.create(level=level, user=user, score=count)
        new_score = instance.score
    elif score.score < int(count):
        score.score = int(count)
        score.save()
        new_score = count
    else:
        new_score = score.score

    return JsonResponse({"Score": new_score, "Level": level})


# ADMIN -----------------------------------------------------------------------
@login_required()
@group_required('ADMIN', 'ENSEIGNANT')
def exportWord(request):
    words = WordOne.objects.filter(level=3)
    for word in words:
        print(word.name)
    return redirect('index')


@login_required()
@group_required('ADMIN', 'ENSEIGNANT')
def createWordOneList(request):
    form = WordFormOneList()
    if request.method == 'POST':
        form = WordFormOneList(request.POST)
        if form.is_valid():
            mots = request.POST['mots'].splitlines()
            groupe = request.POST['group']
            level = request.POST['level']
            nb_mot = 0
            for mot in mots:
                # document = form.save(commit=False)
                if level == "":
                    if len(mot) < 5:
                        level = 1
                    elif len(mot) < 8:
                        level = 2
                    else:
                        level = 3

                mot_existe = WordOne.objects.filter(name=mot, level=level)

                if len(mot_existe) == 0:
                    nb_mot += 1
                    wordModel = WordOne()
                    wordModel.name = mot
                    wordModel.level = level
                    wordModel.save()
                    wordModel.group.set(groupe)

            message = str(nb_mot) + " mots ont été ajoutés avec succès (sur " + str(len(mots)) + ")"
            messages.success(request, message)

            return redirect('games:create_word_list')
    context = {'form': form}
    return render(request, 'games/createWordOneList.html', context)


# JEUX DE LETTRE ----------------------------------------------------------------------------
@login_required()
def letter(request):
    # Filtre par Niveau
    if request.GET.get('l', ''):
        level = request.GET.get('l', '')
    else:
        level = "1"

    user = request.user
    letterScore = LetterScore.objects.filter(user=user, level=level).first()
    if not letterScore:
        letterScore = 0
    else:
        letterScore = letterScore.score
    context_header = {'title': 'Lettres'}

    context = {'level': level,
               'letterScore': letterScore,
               'context_header': context_header,
               }
    return render(request, './games/letter.html', context)


@login_required()
def saveLetterProgress(request):
    level = request.POST.get("level")
    count = request.POST.get("score")
    user = request.user
    score = LetterScore.objects.filter(level=level, user=user).first()
    if not score:
        instance = LetterScore.objects.create(level=level, user=user, score=count)
        new_score = instance.score
    elif score.score < int(count):
        score.score = int(count)
        score.save()
        new_score = count
    else:
        new_score = score.score

    return JsonResponse({"Score": new_score, "Level": level})


# HALO -------------------------------------------------------------------------------------------
@login_required()
def halo(request):
    images = Halo.objects.all()
    context_header = {'title': 'Halo'}

    context = {'images': images,
               'context_header':context_header
               }

    if request.GET.get('p', ''):
        p = request.GET.get('p', '')
        image = Halo.objects.filter(pk=p).first()
        context = {'image': image}

    return render(request, './games/halo.html', context)


# ADDITION -------------------------------------------------------------------------------------------
@login_required()
def addition(request):
    user = request.user
    additionScore = AdditionScore.objects.filter(user=user).first()
    if not additionScore:
        additionScore = 0
    else:
        additionScore = additionScore.score
    context_header = {'title': 'Additions'}
    context = {'additionScore': additionScore, 'context_header': context_header}
    return render(request, './games/addition.html', context)


@login_required()
def addition_posee(request):
    user = request.user
    additionPoseeScore = AdditionPoseeScore.objects.filter(user=user).first()
    if not additionPoseeScore:
        additionPoseeScore = 0
    else:
        additionPoseeScore = additionPoseeScore.score
    context_header = {'title': 'Additions Posées'}
    context = {'additionPoseeScore': additionPoseeScore, 'context_header': context_header}
    return render(request, './games/addition_posee.html', context)


@login_required()
def saveAdditionProgress(request):
    count = request.POST.get("score")
    user = request.user
    score = AdditionScore.objects.filter(user=user).first()
    if not score:
        instance = AdditionScore.objects.create(user=user, score=count)
        new_score = instance.score
    elif score.score < int(count):
        score.score = int(count)
        score.save()
        new_score = count
    else:
        new_score = score.score

    return JsonResponse({"Score": new_score})


@login_required()
def saveAdditionPoseeProgress(request):
    count = request.POST.get("score")
    user = request.user
    score = AdditionPoseeScore.objects.filter(user=user).first()
    if not score:
        instance = AdditionPoseeScore.objects.create(user=user, score=count)
        new_score = instance.score
    elif score.score < int(count):
        score.score = int(count)
        score.save()
        new_score = count
    else:
        new_score = score.score

    return JsonResponse({"Score": new_score})


# MULTIPLICATION -------------------------------------------------------------------------------------------
@login_required()
def multiplication(request):
    user = request.user
    multiplicationScore = MultiplicationScore.objects.filter(user=user).first()
    if not multiplicationScore:
        multiplicationScore = 0
    else:
        multiplicationScore = multiplicationScore.score
    context_header = {'title': 'Multiplications'}
    context = {'multiplicationScore': multiplicationScore, 'context_header':context_header}
    return render(request, './games/multiplication.html', context)


@login_required()
def saveMultiplicationProgress(request):
    count = request.POST.get("score")
    user = request.user
    score = MultiplicationScore.objects.filter(user=user).first()
    if not score:
        instance = MultiplicationScore.objects.create(user=user, score=count)
        new_score = instance.score
    elif score.score < int(count):
        score.score = int(count)
        score.save()
        new_score = count
    else:
        new_score = score.score

    return JsonResponse({"Score": new_score})


# SOUSTRACTION -------------------------------------------------------------------------------------------
@login_required()
def soustraction(request):
    user = request.user
    soustractionScore = SoustractionScore.objects.filter(user=user).first()
    if not soustractionScore:
        soustractionScore = 0
    else:
        soustractionScore = soustractionScore.score
    context_header = {'title': 'Soustractions'}
    context = {'soustractionScore': soustractionScore, 'context_header': context_header}
    return render(request, './games/soustraction.html', context)


@login_required()
def saveSoustractionProgress(request):
    count = request.POST.get("score")
    user = request.user
    score = SoustractionScore.objects.filter(user=user).first()
    if not score:
        instance = SoustractionScore.objects.create(user=user, score=count)
        new_score = instance.score
    elif score.score < int(count):
        score.score = int(count)
        score.save()
        new_score = count
    else:
        new_score = score.score

    return JsonResponse({"Score": new_score})


def journal(request):
    file = os.path.join(settings.MEDIA_ROOT, 'docs/Journal_test.json')
    data = get_journal(file)
    context = {'data': data}

    return render(request, './games/journal.html', context)


def ratp(request):
    try:
        sens = request.GET['s']
    except:
        sens = 'A'

    try:
        station = request.GET['g']
    except:
        station = 'neuilly-plaisance'

    try:
        transport = request.GET['t']
    except:
        transport = 'rers'

    try:
        ligne = request.GET['l']
    except:
        ligne = 'A'

    url = "https://api-ratp.pierre-grimaud.fr/v4/schedules/" + transport + "/" + ligne + "/" + station + "/" + sens
    data = get_json_ratp(url)
    if data != "404":
        infos = []
        for entrie in data['result']['schedules']:
            infos.append({'message': entrie['message'], 'destination': entrie['destination']})

        station = station.replace("-", " ").title()
        context = {'infos': infos, 'station': station}
    else:
        context = {'infos': "404"}
    return render(request, './games/ratp.html', context)
    # return JsonResponse({"Data": data})


@login_required()
@group_required('ADMIN')
@group_required('ENSEIGNANT')
def createHalo(request):
    form = HaloForm()
    if request.method == 'POST':
        form = HaloForm(request.POST, request.FILES)
        if form.is_valid():
            img_url = request.POST['url']

            if img_url != "":
                response = requests.get(img_url)
                if response.status_code == 200:
                    photo = Halo()  # set any other fields, but don't commit to DB (ie. don't save())
                    filename = urlparse(img_url).path.split('/')[-1]
                    extension = filename.split(".")[-1].lower()
                    name = "halo/" + slugify(request.POST['name']) + "." + extension
                    photo.image.save(name, ContentFile(response.content), save=False)
                    photo.image.name = name
                    photo.name = request.POST['name']
                    photo.save()
            else:
                document = form.save(commit=False)
                document.name = request.POST['name']
                document.save()

            message = "Image [" + request.POST['name'] + "] ajoutée avec succès !"
            messages.success(request, message)
            return redirect('games:create_halo')

    context = {'form': form}
    return render(request, 'games/createHalo.html', context)
