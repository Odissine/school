from django import template
from poll.models import *

register = template.Library()


@register.filter(name='random_choices')
def random_choices(question):
    if question.randomize:
        random_choices = question.choices.order_by('?').all()
    else:
        random_choices = question.choices.all()
    return random_choices
