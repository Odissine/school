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
from .models import Word, WordFind, LetterScore, Halo, AdditionScore, MultiplicationScore, SoustractionScore, AdditionPoseeScore
from .forms import WordForm, HaloForm
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
def word(request):

    # Filtre par Classe
    classe = request.user.groups.first()
    user = request.user
    wordDone = WordFind.objects.filter(user=user)
    word_done_list = []
    for word_done in wordDone:
        word_done_list.append(word_done.word)

    if classe.name == "ADMIN" or classe.name == "ENSEIGNANT":
        word_list = Word.objects.all()
    else:
        word_list = Word.objects.filter(group=classe)

    # Filtre par Niveau
    if request.GET.get('l', ''):
        level = request.GET.get('l', '')
    else:
        level = "1"

    word_list = word_list.filter(level=level).order_by('slug')

    if classe.name == "ADMIN" or classe.name == "ENSEIGNANTS":
        classe = "toutes les classes :)"

    context = {'level': level,
               'classe': classe,
               'words': word_list,
               'word_done_list': word_done_list,
               }
    return render(request, './games/word.html', context)


@login_required()
def saveWordProgress(request):
    id = request.POST.get("word")
    word = Word.objects.get(pk=id)
    user = request.user
    progress = WordFind.objects.filter(word=word, user=user)
    print(id, word, user, progress)
    if not progress:
        instance = WordFind.objects.create(word=word, user=user)

    count = WordFind.objects.filter(user=user).count()

    classe = request.user.groups.first()
    if classe.name == "ADMIN" or classe.name == "ENSEIGNANT":
        count_total = Word.objects.all().count()
    else:
        count_total = Word.objects.filter(group=classe).count()

    message = "Bravo ! Tu as trouvé " + str(count) + " mots sur " + str(count_total)
    messages.success(request, message)
    return JsonResponse({"Mots": message})


# ADMIN ----------------------------------------------------------------------------
@login_required()
@group_required('ADMIN')
@group_required('ENSEIGNANT')
def createWord(request):
    form = WordForm()
    if request.method == 'POST':
        form = WordForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.name = request.POST['name']
            document.save()
            message = "Mot ["+request.POST['name'] + "] ajouté avec succès !"
            messages.success(request, message)
            return redirect('games:create_word')

    context = {'form': form}
    return render(request, 'games/createWord.html', context)


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

            message = "Image ["+request.POST['name'] + "] ajoutée avec succès !"
            messages.success(request, message)
            return redirect('games:create_halo')

    context = {'form': form}
    return render(request, 'games/createHalo.html', context)


@login_required()
@group_required('ADMIN')
@group_required('ENSEIGNANT')
def updateWord(request, pk):
    word = Word.objects.get(id=pk)
    form = WordForm(instance=word)
    if request.method == 'POST':
        form = WordForm(request.POST, request.FILES, instance=word)
        if form.is_valid():
            word.level = form.cleaned_data.get('level')
            word.name = form.cleaned_data.get('name')
            if not request.FILES.get('image'):
                print("## ImageField = None")
                print(os.path.join(settings.MEDIA_ROOT, word.image.name))

            document = form.save(commit=False)
            # document.name = request.POST['name']
            # if not form.data['image'] is None:

            # auto_delete_file_on_change(request, instance=word)

            # if request.FILES.get('image'):
            #     print("On supprime le fichier")
            #     word.delete_file()
            # document.save()
            word.save()
            message = "Mot ["+request.POST['name'] + "] edité avec succès !"
            messages.success(request, message)
            return redirect('games:word')
        else:
            context = {'word': word, 'form': form}
    else:
        context = {'form': form}
        return render(request, 'games/createWord.html', context)


@login_required()
@group_required('ADMIN')
@group_required('ENSEIGNANT')
def deleteWord(request, pk):
    word = Word.objects.get(id=pk)
    if request.method == 'POST':
        word.delete()
        message = "Mot ["+request.POST['mot'] + "] edité avec succès !"
        messages.success(request, message)
        return redirect('games:word')

    context = {'word': word}
    return render(request, 'games/deleteWord.html', context)


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

    context = {'level': level,
               'letterScore': letterScore,
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

# HALO
@login_required()
def halo(request):
    images = Halo.objects.all()
    context = {'images': images}

    if request.GET.get('p', ''):
        p = request.GET.get('p', '')
        image = Halo.objects.filter(pk=p).first()
        context = {'image': image}

    return render(request, './games/halo.html', context)


# ADDITION
@login_required()
def addition(request):
    user = request.user
    additionScore = AdditionScore.objects.filter(user=user).first()
    if not additionScore:
        additionScore = 0
    else:
        additionScore = additionScore.score

    context = {'additionScore': additionScore}
    return render(request, './games/addition.html', context)


@login_required()
def addition_posee(request):
    user = request.user
    additionPoseeScore = AdditionPoseeScore.objects.filter(user=user).first()
    if not additionPoseeScore:
        additionPoseeScore = 0
    else:
        additionPoseeScore = additionPoseeScore.score

    context = {'additionPoseeScore': additionPoseeScore}
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


# MULTIPLICATION
@login_required()
def multiplication(request):
    user = request.user
    multiplicationScore = MultiplicationScore.objects.filter(user=user).first()
    if not multiplicationScore:
        multiplicationScore = 0
    else:
        multiplicationScore = multiplicationScore.score

    context = {'multiplicationScore': multiplicationScore}
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


# SOUSTRACTION
@login_required()
def soustraction(request):
    user = request.user
    soustractionScore = SoustractionScore.objects.filter(user=user).first()
    if not soustractionScore:
        soustractionScore = 0
    else:
        soustractionScore = soustractionScore.score

    context = {'soustractionScore': soustractionScore}
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
