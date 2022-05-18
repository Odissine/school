from django import template
from poll.models import *

register = template.Library()


@register.filter(name='create_list')
def create_list(reponses):
    create_list = []
    for reponse in reponses:
        create_list.append(reponse.id)
    return create_list
