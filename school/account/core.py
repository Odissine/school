from django.utils.text import slugify
from games.models import WordScore, LetterScore


def generate_username(firstname, lastname):
    firstname = slugify(firstname)
    lastname = slugify(lastname)
    username = '%s.%s' % (firstname, lastname)
    return username


def generate_email(username, domain):
    email = '%s@%s' % (username, domain)
    return email


def get_moyenne_score(user, type):
    if type == "mot":
        scores = WordScore.objects.filter(user=user)
    else:
        scores = LetterScore.objects.filter(user=user)
    moyenne = 0
    for score in scores:
        moyenne += score.score
    if len(scores) > 0:
        moyenne = round(moyenne / len(scores))
    return moyenne


def get_max_score(user, type):
    if type == "mot":
        scores = WordScore.objects.filter(user=user)
    else:
        scores = LetterScore.objects.filter(user=user)
    max = 0
    for score in scores:
        if score.score > max:
            max = score.score
    return max