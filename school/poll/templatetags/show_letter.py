from django import template

register = template.Library()


@register.filter(name='show_letter')
def show_letter(i):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    return letters[i]
