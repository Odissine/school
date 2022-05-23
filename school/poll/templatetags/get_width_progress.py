from django import template

register = template.Library()


@register.filter(name='get_width_progress')
def get_width_progress(total, value):
    print(total)
    width = round(int(value) * 100 / int(total), 0)
    return int(width)
