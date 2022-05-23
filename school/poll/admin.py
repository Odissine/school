from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportMixin, ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget


# RESOURCES
class AnswerResource(resources.ModelResource):
    class Meta:
        model = Answer


class QuestionResource(resources.ModelResource):
    choices = fields.Field(column_name='choices', attribute='choices', widget=ManyToManyWidget(Answer, field='id'))

    class Meta:
        model = Question
        fields = ('id', 'question', 'description', 'question_pic', 'mandatory', 'multiple', 'randomize', 'choices')


class QuizResource(resources.ModelResource):
    questions = fields.Field(column_name='questions', attribute='questions', widget=ManyToManyWidget(Question, field='question'))

    class Meta:
        model = Quiz
        fields = ("id", "nom", "questions", "status", "published", "date_added", "date_modified")


class QuestionOrderResource(resources.ModelResource):
    class Meta:
        model = QuestionOrder


class UserResponseResource(resources.ModelResource):
    class Meta:
        model = UserResponse

# ADMIN
class AnswerAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'answer', 'answer_pic', 'correct')
    resource_class = AnswerResource


class QuestionAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'question', 'description', 'question_pic', 'mandatory', 'multiple', 'randomize', 'get_choices')
    resource_class = QuestionResource


class QuizAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ("id", "nom", "get_questions", "status", "published", "date_added", "date_modified")
    resource_class = QuizResource


class QuestionOrderAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ("id", "order", "question", "quiz")
    resource_class = QuestionOrderResource


class UserResponseAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ("id", "quiz_instance", "question", "get_responses")
    resource_class = UserResponseResource

admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuestionOrder, QuestionOrderAdmin)
admin.site.register(UserResponse, UserResponseAdmin)

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