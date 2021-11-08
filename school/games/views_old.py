from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Word
from .forms import CreeMot
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def home(request):
    context = {
        'word': Word.objects.all(),
    }
    return render(request, 'games/word.html', context)


class MotListView(ListView):
    model = Word
    template_name = 'games/word.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'word'


class MotCreateView(LoginRequiredMixin, CreateView):
    model = Word
    fields = ['mot', 'image', 'level', 'group']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def group_required(*group_names):

    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


'''
UNE SOLUTION DE DECORATEUR DANS LA VUE

@user_passes_test(core.is_ce1)
def cp_view_bis(request, pk):
    return render(request, './games/word.html')
'''


'''
AUTRE SOLUTION DE DECORATEUR GROUP DANS LA VUE
@group_required('CP')
def cp_mots(request):
    return render(request, './games/word.html')
'''


# JEUX DE MOTS ----------------------------------------------------------------------------
def mots(request):

    # Filtre par Classe
    classe = request.user.groups.first()
    groups = Group.objects.all()
    if classe.name == "ADMIN" or classe.name == "ENSEIGNANT":
        # liste_mots = Mots.objects.filter(group='CP').filter(group='CE1').filter(group='CE2').filter(group='CM1').filter(group='CM2')
        liste_mots = Word.objects.filter(group__name__in=('CP', 'CE1', 'CE2', 'CM1', 'CM2'))
    else:
        liste_mots = Word.objects.filter(group=classe)

    # Filtre par Niveau
    if request.GET.get('l', ''):
        level = request.GET.get('l', '')
    else:
        level = 1
    liste_mots = liste_mots.filter(level=level).order_by('mot')

    if classe.name == "ADMIN" or classe.name == "ENSEIGNANTS":
        classe = "toutes les classes :)"

    context = {'level': level,
               'classe': classe,
               'word': liste_mots,
               }
    return render(request, './games/word.html', context)


# ADMIN ----------------------------------------------------------------------------
@login_required()
@group_required('ADMIN')
@group_required('ENSEIGNANT')
def cree_mots(request):
    if request.method == 'POST':
        form = CreeMot(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.name = request.POST['mot']
            document.save()
            message = "Mot ["+request.POST['mot'] + "] ajouté avec succès !"
            messages.success(request, message)
            return redirect('games:cree_mots')
    else:
        form = CreeMot()
    return render(request, 'games/createWord.html', {
        'form': form
    })


@login_required()
@group_required('ADMIN')
@group_required('ENSEIGNANT')
def edit_mots(request):
    pass
