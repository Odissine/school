from django import template
register = template.Library()

def float2integer(value):
    score = int(value * 100 / 80)
    return score