from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # ADMIN
    path('create_word_list/', views.createWordOneList, name='create_word_list'),
    path('create_halo/', views.createHalo, name='create_halo'),

    # WORD
    path('word_one/', views.wordOne, name='word_one'),
    path('save_word_one/', views.saveWordOneProgress, name='save_word_progress_one'),

    # LETTER
    path('letter/', views.letter, name='letter'),
    path('save_letter/', views.saveLetterProgress, name='save_letter_progress'),

    # HALO
    path('halo/', views.halo, name='halo'),

    # ADDITION
    path('addition/', views.addition, name='addition'),
    path('addition_posee/', views.addition_posee, name='addition_posee'),
    path('save_addition/', views.saveAdditionProgress, name='save_addition_progress'),
    path('save_addition_posee/', views.saveAdditionPoseeProgress, name='save_addition_posee_progress'),

    # MULTIPLICATION
    path('multiplication/', views.multiplication, name='multiplication'),
    path('save_multiplication/', views.saveMultiplicationProgress, name='save_multiplication_progress'),

    # SOUSTRACTION
    path('soustraction/', views.soustraction, name='soustraction'),
    path('save_soustraction/', views.saveSoustractionProgress, name='save_soustraction_progress'),

    # JOURNAL
    path('journal/', views.journal, name='journal'),
    path('ratp/', views.ratp, name='ratp'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)