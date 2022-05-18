from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class Answer(models.Model):
    objects = None
    answer = models.CharField(max_length=200, null=True)
    answer_pic = models.ImageField(upload_to='poll', storage=fs)
    correct = models.BooleanField(default=False)

    def __str__(self):
        if self.answer is not None:
            return self.answer
        else:
            return self.pk


class Question(models.Model):
    objects = None
    question = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=255, null=True)
    question_pic = models.ImageField(upload_to='poll/', storage=fs, null=True)
    choices = models.ManyToManyField(Answer, related_name='QuestionsChoices')
    mandatory = models.BooleanField(default=True)
    multiple = models.BooleanField(default=False)
    randomize = models.BooleanField(default=False)

    def __str__(self):
        if self.question is not None:
            return self.question
        else:
            return self.question_pic

    def get_choices(self):
        return "\n".join([choice.answer for choice in self.choices.all()])


class Theme(models.Model):
    objects = None
    nom = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.nom


class Quiz(models.Model):
    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
        (3, 'Close'),
    )
    nom = models.CharField(max_length=200, null=False)
    theme = models.ForeignKey(Theme, null=False, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, related_name='Quizs')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    published = models.DateTimeField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.nom

    def question_count(self):
        return len(self.questions.all())

    def get_question(self, id):
        return self.questions.all()[id]

    def get_questions(self):
        return "\n".join([question.question for question in self.questions.all()])


class QuestionOrder(models.Model):
    order = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


class QuizInstance(models.Model):
    objects = None
    """
    A combination of user response and a quiz template.
    """
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    start_quiz = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    complete = models.BooleanField(default=False)


class UserResponse(models.Model):
    objects = None
    """
    User response to a single question.
    """
    quiz_instance = models.ForeignKey(QuizInstance, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ManyToManyField(Answer, related_name="UserResponses")
    # time_taken = models.DateTimeField(auto_now_add=True)
    # time_taken_delta = models.DateTimeField(blank=True)
