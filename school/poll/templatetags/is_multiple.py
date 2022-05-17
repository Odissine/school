from django import template
from poll.models import *

register = template.Library()


@register.filter(name='is_multiple')
def is_multiple(question_id):
    question = Question.objets.get(pk=question_id)
    is_multiple = question.multiple
    return is_multiple
