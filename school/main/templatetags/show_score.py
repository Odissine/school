from django import template
from games.models import *
from django.db.models import Avg, Max, Min
register = template.Library()


@register.filter(name='show_score')
def show_score(user, theme):
    if theme == 'lettre':
        score = LetterScore.objects.filter(user=user).aggregate(Max('score'))
    elif theme == 'word':
        score = WordScore.objects.filter(user=user).aggregate(Max('score'))
    elif theme == 'addition':
        score = AdditionScore.objects.filter(user=user).aggregate(Max('score'))
    elif theme == 'soustraction':
        score = SoustractionScore.objects.filter(user=user).aggregate(Max('score'))
    elif theme == 'additionposee':
        score = AdditionPoseeScore.objects.filter(user=user).aggregate(Max('score'))
    elif theme == 'multiplication':
        score = MultiplicationScore.objects.filter(user=user).aggregate(Max('score'))
    else:
        score = {'score__max': 0}
    return score['score__max']
