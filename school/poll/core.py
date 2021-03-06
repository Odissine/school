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


# FONCTION POUR OBTENIR LE SCORE POUR UNE QUESTION DONNEE A L'AIDE DES REPONSES DES UTILISATEURS vs REPONSES CORRECTES
def get_score(user_rep, correct_rep):
    score = 0
    if user_rep == correct_rep:
        score = 2
    if len(user_rep) < len(correct_rep):
        if any(x in user_rep for x in correct_rep):
            score = 1
    return score
