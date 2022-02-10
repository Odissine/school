from django import template
register = template.Library()

def float2integer(value,arg):
    score = int(value * 100 / arg)
    return score
