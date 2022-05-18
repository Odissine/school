from django.shortcuts import render

from .forms import *
from .core import *
from .models import Quiz, Question, Answer
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls.base import reverse
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import user_passes_test, login_required


# ##########################################################################################
# QUIZ
# ##########################################################################################

# SHOW LISTING ##################################################################################
def show_list(request):
    quizs = Quiz.objects.all()
    context = {
        'quizs': quizs,
    }
    return render(request, "poll/show_list.html", context)


def show_quiz(request, quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
    except:
        messages.error(request, "Ce quiz n'existe pas ;)")
        return redirect('poll:show-list')
    context = {
        'quiz': quiz,
    }
    return render(request, "poll/show_quiz.html", context)


@login_required()
def answer_quiz(request):
    context = {}
    score = 0
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=request.POST.get('id_quiz'))
        player = request.user
        quiz_player = QuizInstance.objects.filter(player=player, quiz=quiz)

        if len(quiz_player) == 0:
            dic_answer = sort_answer(request.POST.getlist("reponse"), quiz)
            # Creation de l'instance
            quiz_instance = QuizInstance.objects.create(player=player, quiz=quiz)

            # Question ajouté a l'instance pour l'utilisateur
            for question in quiz.questions.all():
                user_reponse = UserResponse.objects.create(quiz_instance=quiz_instance, question=question)
                for r in dic_answer[question.id]:
                    answer = Answer.objects.get(pk=r)
                    user_reponse.response.add(answer)
                nb_correct_answer = len(question.choices.filter(correct=True))
                lt = sorted(list(question.choices.filter(correct=True).values_list('pk')))
                out = [item for t in lt for item in t]
                if len(dic_answer[question.id]) < nb_correct_answer:
                    if sorted(dic_answer[question.id]) == out:
                        print(sorted(dic_answer[question.id]), out)
                        score += 2
                    if any(x in dic_answer[question.id] for x in out):
                        print(sorted(dic_answer[question.id]), out)
                        score += 1

                if len(dic_answer[question.id]) == nb_correct_answer:
                    if sorted(dic_answer[question.id]) == out:
                        print(sorted(dic_answer[question.id]), out)
                        score += 2

            print(score)
            quiz_instance.score = score
            quiz_instance.save()
        else:
            context = {
                'error': True,
            }
    return render(request, "poll/answer_quiz.html", context)


# ADMIN LISTING ##################################################################################
def quiz_list(request):
    quizs = Quiz.objects.all()
    context = {
        'quizs': quizs,
    }
    return render(request, "poll/admin_quiz.html", context)


# CREATION #################################################################################
def quiz_create(request):
    if request.user.is_staff:
        title = "Créer un Quiz"
        form = QuizForm()
        previous_page = reverse('poll:quiz-list')
        formAction = 'poll:quiz-create'

        if request.method == 'POST':
            form = QuizForm(request.POST, request.FILES)

            if form.is_valid():
                obj = form.save()

                message = "Quiz créée !"
                messages.success(request, message)
                return redirect('poll:question-create', quiz_id=obj.id)
            else:
                message = "Une erreur s'est produite"
                messages.error(request, message)
            return redirect('poll:quiz-create')

        context = {
            'form': form,
            'title': title,
            'formAction': formAction,
            'previous_page': previous_page,
        }
        return render(request, "poll/create_quiz.html", context)
    else:
        messages.error(request, "Vous n'avez pas les droits !")
        return redirect('poll:quiz-list')


# START ####################################################################################
def quiz_start(request):
    pass


# ##########################################################################################
# QUESTIONS
# ##########################################################################################

# LISTING ##################################################################################
def question_list(request, quiz_id=None, question_id=None):
    if quiz_id is None:
        questions = Question.objects.all()
        quiz = None
    else:
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            questions = quiz.questions.all()
        except:
            quiz = None
            questions = Question.objects.all()
    try:
        question = Question.objects.get(pk=question_id)
    except:
        question = None
    formQuestion = QuestionForm(instance=question)
    formQuestionPic = QuestionPicForm(instance=question)
    formQuiz = QuizQuestionForm(instance=quiz)
    formAnswerPic = AnswerPicForm()
    context = {
        'quiz': quiz,
        'question': question,
        'questions': questions,
        'formQuestion': formQuestion,
        'formQuestionPic': formQuestionPic,
        'formQuiz': formQuiz,
        'formAnswerPic': formAnswerPic,
    }
    return render(request, "poll/admin_question.html", context)


# CREATION #################################################################################
def question_create(request, quiz_id=None):
    if request.user.is_staff:
        title = "Créer une question"
        form = QuestionForm()
        previous_page = reverse('poll:quiz-list')
        formAction = 'poll:question-create'
        try:
            quiz = Quiz.objects.get(pk=quiz_id)
        except:
            quiz = None
        if request.method == 'POST':
            form = QuestionForm(request.POST, request.FILES)
            form_answer = AnswerForm(request.POST, request.FILES)

            if form.is_valid():
                if not form.cleaned_data['question'] and form.cleaned_data['question_pic'] is None:
                    message = "Le champ question ou illustration doit être renseigné !"
                    messages.error(request, message)
                    return redirect('poll:question-create', quiz_id=quiz_id)

                obj = form.save()
                if quiz is not None:
                    quiz.questions.add(obj)
                    quiz.save()

                message = "Question créée !"
                messages.success(request, message)
                return redirect('poll:answer-create', question_id=obj.id)
            else:
                message = "Une erreur s'est produite"
                messages.error(request, message)
            return redirect('poll:question-create', quiz_id=quiz_id)

        context = {
            'quiz': quiz,
            'form': form,
            'title': title,
            'formAction': formAction,
            'previous_page': previous_page,
        }
        return render(request, "poll/create_question.html", context)
    else:
        messages.error(request, "Vous n'avez pas les droits !")
        return redirect('poll:quiz-list')


# EDITION ##################################################################################
def question_edit(request, question_id):
    if request.method == 'POST':
        question_input = request.POST.get('question_input')
        description_input = request.POST.get('description_input')
        question = Question.objects.get(pk=question_id)
        if question_input is not None:
            question.question = question_input
            question.save()

        if description_input is not None:
            question.description = description_input
            question.save()

        return HttpResponse(question)


# SUPPRESSION
def question_delete(request, quiz_id=None, question_id=None):
    try:
        question = Question.objects.get(pk=question_id)
    except:
        messages.error(request, "Question inexistante !")
        return redirect('poll:question-list', quiz_id=quiz_id, question_id=None)

    question.delete()
    messages.success(request, "Question supprimée !")
    return redirect('poll:question-list', quiz_id=quiz_id, question_id=None)


# ACTIVATION/DESACTIVATION CHOIX MULTIPLE QUESTION #########################################
def question_edit_options(request, question_id, checked, mode):
    if checked == "true":
        checked = True
    else:
        checked = False
    try:
        question = Question.objects.get(pk=question_id)
    except:
        question = None

    if question is not None:
        if mode == "multiple":
            question.multiple = checked

            if checked is False:
                answers = question.choices.all()
                last_answer = question.choices.filter(correct=True).last()
                for answer in answers:
                    answer.correct = False
                    answer.save()
                last_answer.correct = True
                last_answer.save()

        if mode == "mandatory":
            question.mandatory = checked
        if mode == "randomize":
            question.randomize = checked
        question.save()

    return HttpResponse(checked)


# AJOUT ILLUSTRATION #######################################################################
def question_add_pic(request, question_id=None):
    if request.method == 'POST' and question_id is not None:
        question = Question.objects.get(pk=question_id)
        form = QuestionPicForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            if not form.cleaned_data['question_pic'] is None:
                if question.question_pic is None:
                    obj = form.save()
                else:
                    if os.path.isfile(question.question_pic.path):
                        os.remove(question.question_pic.path)
                    obj = form.save()
                message = "Image ajoutée !"
                messages.success(request, message)
                return redirect('poll:question-list', question_id=question.id)
        else:
            message = "Une erreur s'est produite"
            messages.error(request, message)
        return redirect('poll:question-list', question_id=question.id)


# EDITION ILLUSTRATION #####################################################################
def question_edit_pic(request):
    if request.method == 'POST':
        question = Question.objects.get(pk=request.POST.get("question_input"))
        if not request.POST.get("question_pic") is None:
            question.question_pic = request.POST.get("question_pic")
            question.save()
            message = "Image ajoutée !"
            messages.success(request, message)
            return redirect('poll:question-list', question_id=question.id)

        message = "Une erreur s'est produite"
        messages.error(request, message)
    return redirect('poll:question-list', question_id=question.id)


# SUPPRESSION ILLUSTRATION #################################################################
def question_delete_pic(request):
    if request.POST:
        question = Question.objects.get(pk=request.POST.get('question_input'))
        if question.question_pic:
            if os.path.isfile(question.question_pic.path):
                os.remove(question.question_pic.path)
            question.question_pic = ""
            question.save()

    return HttpResponse(question)


# ASSOCIER QUESTION
def question_add(request, quiz_id):
    if request.POST:
        quiz = Quiz.objects.get(pk=quiz_id)
        form = QuizQuestionForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Questions mises à jour !")
            return redirect('poll:question-list', quiz_id=quiz_id, question_id=None)

    messages.error(request, "Une erreur s'est produite !")
    return redirect('poll:question-list', quiz_id=quiz_id, question_id=None)


# ##########################################################################################
# REPONSES
# ##########################################################################################

# CREATIONS ################################################################################
def answer_create(request, question_id=None):
    if request.user.is_staff:
        title = "Ajouter les réponses (choix)"
        form = AnswerForm()
        formAction = 'poll:answer-create'
        AnswerFormSet = formset_factory(AnswerForm, formset=BaseAnswerFormSet)
        answer_formset = AnswerFormSet()
        question = None
        if question_id is not None:
            try:
                question = Question.objects.get(pk=question_id)
                previous_page = reverse('poll:question-list', args=(question_id,))
            except:
                question = None
                previous_page = reverse('poll:question-list', args=(None,))
        if request.method == 'POST':
            try:
                question_id = request.POST.get("question")
                question = Question.objects.get(pk=question_id)
            except:
                question = None

            form = AnswerForm(request.POST, request.FILES)
            answer_formset = AnswerFormSet(request.POST, request.FILES)

            if answer_formset.is_valid():
                for answer_form in answer_formset:
                    answer = answer_form.cleaned_data.get('answer')
                    answer_pic = answer_form.cleaned_data.get('answer_pic')
                    correct = answer_form.cleaned_data.get('correct')
                    obj_answer = answer_form.save()
                    if question is not None:
                        if question.multiple is False and correct is True:
                            for ans in question.choices.all():
                                ans.correct = False
                                ans.save()
                        question.choices.add(obj_answer)
                        question.save()
                messages.success(request, "Reponses créées avec succès !")
                return redirect('poll:question-list', question_id=question.id)

        context = {
            'form': form,
            'answer_formset': answer_formset,
            'title': title,
            'formAction': formAction,
            'previous_page': previous_page,
            'question': question,
        }
        return render(request, "poll/create_answer.html", context)

    else:
        messages.error(request, "Vous n'avez pas les droits !")
        return redirect('poll:quiz-list')


# CHANGEMENT REPONSE CORRECT ###############################################################
def answer_edit_correct(request, question_id, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except:
        answer = None
    try:
        question = Question.objects.get(pk=question_id)
    except:
        question = None
    if question is not None:
        answers = question.choices.all()
        if answer is not None:
            if answer.correct is False:
                # On remet tout à FALSE pour ne mettre que celle selectionnée à TRUE
                if question.multiple is False:
                    print("Une seule réponse")
                    for ans in answers:
                        ans.correct = False
                        ans.save()
                answer.correct = True
            else:
                is_correct_exist = False
                for ans in answers:
                    if ans.correct is True:
                        is_correct_exist = True
                        break
                if is_correct_exist is True:
                    answer.correct = False
            answer.save()
    return HttpResponse(answer)


# EDITION REPONSE ##########################################################################
def answer_edit_text(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
    except:
        answer = None
    try:
        answer_text = request.POST.get("answer_input")
    except:
        answer_text = None
        answer = None

    if answer is not None and answer_text is not None:
        answer.answer = answer_text
        answer.save()

    return HttpResponse(answer)


# AJOUT/EDITION ILLUSTRATION REPONSE #######################################################
def answer_edit_pic(request, question_id, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerPicForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            if not form.cleaned_data['answer_pic'] is None:
                if answer.answer_pic is None:
                    obj = form.save()
                else:
                    if os.path.isfile(answer.answer_pic.path):
                        os.remove(answer.answer_pic.path)
                    obj = form.save()
                message = "Image ajoutée !"
                messages.success(request, message)
                return redirect('poll:question-list', question_id=question_id)
        else:
            message = "Une erreur s'est produite"
            messages.error(request, message)
        return redirect('poll:question-list', question_id=question_id)


# SUPPRESSION REPONSE ######################################################################
def answer_delete(request):
    try:
        answer_id = request.POST.get("choice_input")
    except:
        answer_id = None

    try:
        answer = Answer.objects.get(pk=answer_id)
    except:
        answer = None

        answer = None

    if answer is not None and answer_id is not None:
        answer.delete()

    return HttpResponse(answer)


# ##########################################################################################
# THEME
# ##########################################################################################

# CREATION #################################################################################
def theme_create(request):
    if request.user.is_staff:
        title = "Créer un Thème"
        form = ThemeForm()
        previous_page = reverse('poll:quiz-list')
        formAction = 'poll:theme-create'

        if request.method == 'POST':
            form = ThemeForm(request.POST)

            if form.is_valid():
                obj = form.save()

                message = "Theme créée !"
                messages.success(request, message)
                return redirect('poll:quiz-create')
            else:
                message = "Une erreur s'est produite"
                messages.error(request, message)
            return redirect('poll:theme-create')

        context = {
            'form': form,
            'title': title,
            'formAction': formAction,
            'previous_page': previous_page,
        }
        return render(request, "poll/create_theme.html", context)
    else:
        messages.error(request, "Vous n'avez pas les droits !")
        return redirect('poll:quiz-list')


# LISTING ##################################################################################

def theme_list(request):
    themes = Theme.objects.all()
    context = {
        'themes': themes,
    }
    return render(request, "poll/admin_theme.html", context)


# EDITION ##################################################################################
def theme_edit(request, theme_id):
    pass


# SUPPRESSION ##############################################################################
def theme_delete(request, theme_id):
    pass


# ##########################################################################################
# USER
# ##########################################################################################

# AFFICHAGE DES JOUEURS ####################################################################
def show_quiz_user_list(request, quiz_id=None):
    title = "Liste des joueurs"
    try:
        quiz = Quiz.objects.get(pk=quiz_id)
        instances = QuizInstance.objects.filter(quiz=quiz)
    except:
        instances = QuizInstance.objects.all()
    instances = list(set(instances))
    print(len(instances))
    context = {
        'instances': instances,
        'title': title,
    }
    return render(request, "poll/show_quiz_user_list.html", context)


# AFFICHAGE D'UN JOUEUR ####################################################################
def show_player(request, player_id, quiz_id):
    player = User.objects.get(pk=player_id)
    quiz = Quiz.objects.get(pk=quiz_id)
    instance = QuizInstance.objects.get(player=player, quiz=quiz)
    reponses = UserResponse.objects.filter(quiz_instance=instance)

    context = {
        'player': player,
        'quiz': quiz,
        'instance': instance,
        'reponses': reponses,
    }
    return render(request, "poll/show_player.html", context)
