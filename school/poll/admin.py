from django.contrib import admin
from .models import *


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'description', 'question_pic', 'mandatory', 'multiple', 'randomize', 'get_choices']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer', 'answer_pic', 'correct']
