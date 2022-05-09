from .models import *
from django import forms
from django_select2.forms import Select2Widget, Select2MultipleWidget
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError


class QuestionPicForm(forms.ModelForm):
    question_pic = forms.ImageField(
        label="Illustration : ",
        widget=forms.FileInput(attrs={'class': 'form-control', 'oninput': 'question_pic_preview.src = window.URL.createObjectURL(this.files[0])'}),
        required=False,
        help_text='Choisir une illustration',
    )

    def __init__(self, *args, **kwargs):
        self.question_pic = kwargs.pop('question_pic', None),
        super(QuestionPicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['question_pic']


class AnswerPicForm(forms.ModelForm):
    answer_pic = forms.ImageField(
        label="Illustration : ",
        widget=forms.FileInput(attrs={'class': 'form-control', 'oninput': 'answer_pic_preview.src = window.URL.createObjectURL(this.files[0])'}),
        required=False,
        help_text='Choisir une illustration',
    )

    def __init__(self, *args, **kwargs):
        self.answer_pic = kwargs.pop('answer_pic', None),
        super(AnswerPicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['answer_pic']


class QuestionForm(forms.ModelForm):
    question = forms.CharField(
        widget=forms.TextInput(attrs={'size': 20, 'class': 'form-control'}),
        label="Question :",
        required=False,
        help_text='Intitulé de la question',
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class': 'form-control'}),
        label="Description :",
        required=False,
        help_text='Description de la question (obligatoire)',
    )
    question_pic = forms.ImageField(
        label="Illustration : ",
        widget=forms.FileInput(attrs={'class': 'form-control', 'oninput': 'question_pic_preview.src = window.URL.createObjectURL(this.files[0])'}),
        required=False,
        help_text='Choisir une illustration',
    )

    mandatory = forms.BooleanField(
        label="Réponse obligatoire ?",
        initial=True,
        required=False,
        help_text='Question obligatoire ou pas ?',
    )

    multiple = forms.BooleanField(
        label="Plusieurs réponses possible ?",
        initial=False,
        required=False,
        help_text='Plusieurs réponses possible ?',
    )

    randomize = forms.BooleanField(
        label="Affichage aléatoire des réponses ?",
        initial=False,
        required=False,
        help_text='Affichage aléatoire des réponses ?',
    )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None),
        self.question_pic = kwargs.pop('question_pic', None),
        self.description = kwargs.pop('description', None),
        self.mandatory = kwargs.pop('mandatory', None),
        self.multiple = kwargs.pop('multiple', None),
        self.randomize = kwargs.pop('randomize', None),
        super(QuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ['question', 'description', 'question_pic', 'mandatory', 'multiple', 'randomize']


class AnswerForm(forms.ModelForm):
    answer = forms.CharField(
        widget=forms.TextInput(attrs={'size': 20, 'class': 'form-control'}),
        label="Réponse :",
        required=False,
        help_text="Réponse possible au format texte",
    )
    answer_pic = forms.ImageField(
        widget=forms.FileInput(attrs={'size': 20, 'class': 'form-control preview-image', 'data': 'preview'}),
        required=False,
        label="Illustration : ",
        help_text="Choisir une image pour illustrer ou remplacer la réponse",
    )
    correct = forms.BooleanField(
        initial=False,
        required=False,
        label="Réponse correcte",
    )

    def __init__(self, *args, **kwargs):
        self.answer = kwargs.pop('answer', None),
        self.answer_pic = kwargs.pop('answer_pic', None),
        self.correct = kwargs.pop('correct', None),
        super(AnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['answer', 'answer_pic', 'correct']


class ThemeForm(forms.ModelForm):
    nom = forms.CharField(
        widget=forms.TextInput(),
        label="Theme :",
        required=True,
        help_text='Nom du thème',
    )

    def __init__(self, *args, **kwargs):
        self.answenomr = kwargs.pop('nom', None),
        super(ThemeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Theme
        fields = ['nom']


class QuizForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions', None),
        super(QuizForm, self).__init__(*args, **kwargs)

    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
        (3, 'Close'),
    )
    nom = forms.CharField(
        label='Titre',
        widget=forms.TextInput(attrs={'style': 'width:80%'}),
        required=True,
        help_text='Titre du quiz',
    )
    theme = forms.ModelChoiceField(
        label="Thème : ",
        required=False,
        queryset=Theme.objects.all(),
        widget=Select2Widget(attrs={'placeholder': 'Thème', 'class': 'form-control js-example-basic-single', 'style': 'width:80%'}),
        help_text='Choisir un thème',
    )

    questions = forms.ModelMultipleChoiceField(
        label="Questions : ",
        required=False,

        queryset=Question.objects.all(),
        widget=Select2MultipleWidget(attrs={'placeholder': 'Questions', 'class': 'form-control js-example-basic-single', 'style': 'width:80%; z-index:1056; position:relative;'}),
        help_text='Choisir une ou plusieurs questions',
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        initial=1,
        required=False,
        widget=Select2Widget(attrs={'placeholder': 'Thème', 'class': 'form-control js-example-basic-single', 'style': 'width:80%'}),
        help_text='Choisir un statut (Brouillon par défaut)',
    )

    class Meta:
        model = Quiz
        fields = ['nom', 'theme', 'questions', 'status']


class QuizQuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions', None),
        super(QuizQuestionForm, self).__init__(*args, **kwargs)

    questions = forms.ModelMultipleChoiceField(
        label="Questions : ",
        required=False,
        queryset=Question.objects.all(),
        widget=Select2MultipleWidget(attrs={'placeholder': 'Questions', 'class': 'form-control js-example-basic-single', 'style': 'width:80%; z-index:1056; position:relative;'}),
        help_text='Choisir une ou plusieurs questions',
    )

    class Meta:
        model = Quiz
        fields = ['questions']


class BaseAnswerFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        answers = []
        answers_pic = []
        corrects = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                answer = form.cleaned_data['answer']
                answer_pic = form.cleaned_data['answer_pic']
                correct = form.cleaned_data['correct']

                # Check that no two links have the same anchor or URL
                if answer or answer_pic:
                    answers.append(answer)
                    answers_pic.append(answer_pic)
                    corrects.append(correct)
