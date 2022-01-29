from .models import WordOne


def word_allready_present(word):
    word_test = WordOne.objects.filter(name=word)
    print(word_test)