from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportMixin, ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget


class AnswerResource(resources.ModelResource):
    class Meta:
        model = Answer


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        widget = ManyToManyWidget(Answer, field='answer')


class QuizResource(resources.ModelResource):
    class Meta:
        model = Quiz


class QuestionOrderResource(resources.ModelResource):
    class Meta:
        model = QuestionOrder


@admin.register(Answer)
class AnswerAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'answer', 'answer_pic', 'correct')
    resource_class = AnswerResource


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'question', 'description', 'question_pic', 'mandatory', 'multiple', 'randomize', 'get_choices')
    resource_class = QuestionResource


@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ("id", "nom", "get_questions", "status", "published", "date_added", "date_modified")
    resource_class = QuizResource


@admin.register(QuestionOrder)
class QuestionOrderAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ("id", "order", "question", "quiz")
    resource_class = QuestionOrderResource


'''
class AnswerAdmin(ImportMixin, admin.ModelAdmin):
    class AnswerResource(resources.ModelResource):
        class Meta:
            model = Answer
            fields = ("id", "answer", "answer_pic", "correct")
    resource_class = AnswerResource


class QuestionAdmin(ImportMixin, admin.ModelAdmin):
    class QuestionResource(resources.ModelResource):
        class Meta:
            model = Question
            fields = ("id", "question", "description", "question_pic", "choices", "mandatory", "multiple", "randomize")
    resource_class = QuestionResource


class QuizAdmin(ImportMixin, admin.ModelAdmin):
    class QuizResource(resources.ModelResource):
        class Meta:
            model = Quiz
            fields = ("id", "nom", "questions", "status", "published", "date_added", "date_modified")
    resource_class = QuizResource


class QuestionOrderAdmin(ImportMixin, admin.ModelAdmin):
    class QuestionOrderResource(resources.ModelResource):
        class Meta:
            model = QuestionOrder
            fields = ("id", "order", "question", "quiz")
    resource_class = QuestionOrderResource


admin.site.register(Answer,AnswerAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Quiz,QuizAdmin)
admin.site.register(QuestionOrder,QuestionOrderAdmin)
'''