from django import template
from poll.models import *

register = template.Library()


@register.filter(name='is_answer_pic')
def is_answer_pic(question):
    answers = question.choices.all()
    is_pic = False
    for answer in answers:
        if answer.answer_pic is not None and answer.answer_pic != "":
            is_pic = True
            break
    return is_pic
