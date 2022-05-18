import os
from .models import *


def delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


def sort_answer(reponses, quiz):
    dic_questions = {}
    for question in quiz.questions.all():
        dic_questions[question.id] = []

    for reponse in reponses:
        qs = Question.objects.filter(choices__id=reponse)
        for q in qs:
            dic_questions[q.id].append(int(reponse))

    return dic_questions
