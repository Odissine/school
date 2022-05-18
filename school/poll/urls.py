from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from .views import *
import os

app_name = 'poll'

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

urlpatterns = [

    # SHOW
    path('show/list', show_list, name='show-list'),
    path('show/quiz/<quiz_id>', show_quiz, name='show-quiz'),
    path('answer/quiz', answer_quiz, name='answer-quiz'),

    # QUIZ
    path('quiz/create', quiz_create, name='quiz-create'),
    path('quiz/list', quiz_list, name='quiz-list'),
    path('quiz/start/<quiz_id>', quiz_start, name='quiz-start'),

    # QUESTIONS
    path('question/list/<quiz_id>/<question_id>', question_list, name='question-list'),
    path('question/list/<question_id>', question_list, name='question-list'),
    path('question/create/<quiz_id>', question_create, name='question-create'),
    path('question/add/<quiz_id>', question_add, name='question-add'),
    path('question/edit/<question_id>', question_edit, name='question-edit'),
    path('question/edit/<quiz_id>/<question_id>', question_edit, name='question-edit'),
    path('question/delete/<question_id>', question_delete, name='question-delete'),
    path('question/delete/<quiz_id>/<question_id>', question_delete, name='question-delete'),
    path('question/delete/pic', question_delete_pic, name='question-delete-pic'),
    path('question/add/pic/<question_id>', question_add_pic, name='question-add-pic'),
    path('question/edit/<question_id>/<checked>/<mode>', question_edit_options, name='question-edit-options'),

    path('question_pic/edit', question_edit_pic, name='question-edit-pic'),

    # REPONSES
    path('answer/create/<question_id>', answer_create, name='answer-create'),
    path('answer/edit/correct/<question_id>/<answer_id>', answer_edit_correct, name='answer-edit-correct'),
    path('answer/edit/text/<answer_id>', answer_edit_text, name='answer-edit-text'),
    path('answer/edit/pic/<question_id>/<answer_id>', answer_edit_pic, name='answer-edit-pic'),
    path('answer/delete', answer_delete, name='answer-delete'),



    path('theme/create/', theme_create, name='theme-create'),
    path('theme/edit/<theme_id>', theme_edit, name='theme-edit'),
    path('theme/delete/<theme_id>', theme_delete, name='theme-delete'),
    path('theme/list/', theme_list, name='theme-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
