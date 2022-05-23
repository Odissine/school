from django import template
from poll.models import *

register = template.Library()


@register.filter(name='score_max')
def random_choices(quiz):
    # Version avec point en moins si mauvaise réponse
    '''
    questions = quiz.questions.all()
    score_max = 0
    for question in questions:
        for choice in question.choices.all():
            if choice.correct:
                score_max += 1
    '''
    # Version avec 2pts si bonne réponse, 1 pt si réponse incomplète, 0 si mauvaises réponses ou trop de réponses
    questions = quiz.questions.all()
    score_max = len(questions) * 2
    return score_max
