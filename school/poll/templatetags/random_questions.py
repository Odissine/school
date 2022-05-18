from django import template
from poll.models import *

register = template.Library()


@register.filter(name='random_questions')
def random_choices(quiz):
    random_questions = quiz.questions.order_by('?').all()
    return random_questions
