from django import template
from poll.models import *

register = template.Library()


@register.filter(name='color')
def color(group):
    color_class = {'ADMIN': 'bg-secondary', 'CP': 'bg-primary', 'CE1': 'bg-primary', 'CE2': 'bg-warning', 'CM1': 'bg-warning', 'CM2': 'bg-danger', 'ELEVE': 'bg-secondary'}
    color = color_class[group]
    return color
