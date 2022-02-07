from django.shortcuts import render, redirect
from django.db.models import Avg, Max, Min
from games.models import LetterScore, WordScore, AdditionScore, AdditionPoseeScore, SoustractionScore, MultiplicationScore
from main.core import get_purcent

def index_view(request):

    # lettre_moyenne = LetterScore.objects.filter(user__group=request.user.groups.first()).all()
    # print(lettre_moyenne)
    max_score_letter = LetterScore.objects.filter(user__groups=request.user.groups.first()).aggregate(Max('score'))
    score_letter = LetterScore.objects.filter(user=request.user).aggregate(Max('score'))
    score_letter_purcent = get_purcent(score_letter['score__max'], max_score_letter['score__max'])

    max_score_word = WordScore.objects.filter(user__groups=request.user.groups.first()).aggregate(Max('score'))
    score_word = WordScore.objects.filter(user=request.user).aggregate(Max('score'))
    score_word_purcent = get_purcent(score_word['score__max'],max_score_word['score__max'])

    max_score_addition = AdditionScore.objects.filter(user__groups=request.user.groups.first()).aggregate(Max('score'))
    score_addition = AdditionScore.objects.filter(user=request.user).aggregate(Max('score'))
    score_addition_purcent = get_purcent(score_addition['score__max'],max_score_addition['score__max'])

    max_score_additionposee = AdditionPoseeScore.objects.filter(user__groups=request.user.groups.first()).aggregate(Max('score'))
    score_additionposee = AdditionPoseeScore.objects.filter(user=request.user).aggregate(Max('score'))
    score_additionposee_purcent = get_purcent(score_additionposee['score__max'],max_score_additionposee['score__max'])

    max_score_soustraction = SoustractionScore.objects.filter(user__groups=request.user.groups.first()).aggregate(Max('score'))
    score_soustraction = SoustractionScore.objects.filter(user=request.user).aggregate(Max('score'))
    score_soustraction_purcent = get_purcent(score_soustraction['score__max'],max_score_soustraction['score__max'])

    max_score_multiplication = MultiplicationScore.objects.filter(user__groups=request.user.groups.first()).aggregate(Max('score'))
    score_multiplication = MultiplicationScore.objects.filter(user=request.user).aggregate(Max('score'))
    score_multiplication_purcent = get_purcent(score_multiplication['score__max'],max_score_multiplication['score__max'])
    
    


    context_header = {'title': ''}
    context = {'context_header': context_header,
               'max_score_letter': max_score_letter['score__max'],
               'score_letter': score_letter['score__max'],
               'max_score_word': max_score_word['score__max'],
               'score_word': score_word['score__max'],
               'max_score_addition': max_score_addition['score__max'],
               'score_addition': score_addition['score__max'],
               'max_score_additionposee': max_score_additionposee['score__max'],
               'score_additionposee': score_additionposee['score__max'],
               'max_score_soustraction': max_score_soustraction['score__max'],
               'score_soustraction': score_soustraction['score__max'],
               'max_score_multiplication': max_score_multiplication['score__max'],
               'score_multiplication': score_multiplication['score__max'],
               'score_letter_purcent':score_letter_purcent,
               'score_word_purcent':score_word_purcent,
               'score_addition_purcent':score_addition_purcent,
               'score_additionposee_purcent':score_additionposee_purcent,
               'score_soustraction_purcent':score_soustraction_purcent,
               'score_multiplication_purcent':score_multiplication_purcent,
               }
    return render(request, 'main/index.html', context)