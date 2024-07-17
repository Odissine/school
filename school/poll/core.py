import os
from .models import *
from django.contrib.auth.models import User, Group

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
    elif len([i for i in user_rep if i in correct_rep]) > 0 or len([i for i in correct_rep if i in user_rep]) > 0:
        score = 1
    return score

def update_score(user_rep, correct_rep, instance):
    score = 0
    if user_rep == correct_rep:
        score = 2
    elif len([i for i in user_rep if i in correct_rep]) > 0 or len([i for i in correct_rep if i in user_rep]) > 0:
        score = 1
    instance.score = score
    instance.save()
    return score

def get_questions(quiz):
    return quiz.questions.all()

    
def get_answers(question):
    return list(question.choices.all())
    

def get_correct_answers(question):
    return list(question.choices.filter(correct=True))


def get_quiz_instance(player, quiz):
    try:
        quiz_instance = QuizInstance.objects.get(player=player, quiz=quiz)
    except:
        quiz_instance = None
    return quiz_instance


def get_user_responses(quiz_instance, question):
    try:
        obj = UserResponse.objects.get(quiz_instance=quiz_instance, question=question)
        return list(obj.response.all())
    except:
        return []
        

def reset_score():
    quizs = Quiz.objects.all()
    players = User.objects.all()
    for player in players:
        for quiz in quizs:
            score = 0
            quiz_instance = get_quiz_instance(player, quiz)
            # print(quiz_instance.complete)
            if quiz_instance:
                if quiz_instance.complete is False:
                    continue
                questions = get_questions(quiz)
                for question in questions:
                    choices = get_answers(question)
                    corrects = get_correct_answers(question)
                    user_responses = get_user_responses(quiz_instance, question)
                    
                    # TOUT EST COCHE ALORS QUE TOUTES LES REPONSES NE SONT PAS BONNES
                    # print(player, quiz, question, len(corrects), len(choices), len(user_responses))
                    # print((x.nom) for x in corrects, "vs", ((y.nom) for y in user_responses)
                    # print("correct")
                    # [print(x.pk) for x in corrects]
                    # print("reponses données")
                    # [print(x.pk) for x in user_responses]
                    if len(user_responses) == len(choices) and len(corrects) < len(choices):
                        print("Tout faux")
                        continue
                    if user_responses == corrects:
                        print("Tout bon")
                        score += 2
                        continue
                    if all(item in corrects for item in user_responses):
                        print("Une bonne réponse (pas assez de réponse)")
                        score += 1
                        continue
                    if all(item in user_responses for item in corrects):
                        print("Une bonne réponse (trop de réponse)")
                        score += 1
                        continue
                    # any(item in user_responses for item in corrects)
                    if any(item in user_responses for item in corrects):
                        print("Pas tout a fait juste mais bon nombre de réponse")
                        score += 1
                        continue
                    if not any(item in user_responses for item in corrects):
                        print("Aucune bonne réponse")
                        continue
                print(player, quiz, score)
                quiz_instance.score = score
                quiz_instance.save()
    return True


def nouvelle_annee():
    classes = ['ELEVE', 'CM2', 'CM1', 'CE2', 'CE1', 'CP']
    for i in range(1,6):
        groupe = Group.objects.get(name=classes[i])
        groupe_to_change = Group.objects.get(name=classes[i-1])
        users = User.objects.filter(groups__name=classes[i])
        # print(classes[i], groupe, classes[i-1])
        # print(users)
        # print("#########")
        
        for user in users:
            user_group = User.groups.through.objects.get(user=user)
            user_group.group = groupe_to_change
            # user.groups.set(groupe_to_change)
            user_group.save()
        print(classes[i], " to ", classes[i-1], " Done")
            



