from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # ADMIN
    path('create_word/', views.createWord, name='create_word'),
    path('create_halo/', views.createHalo, name='create_halo'),
    path('update_word/<str:pk>/', views.updateWord, name='update_word'),
    path('delete_word/<str:pk>/', views.deleteWord, name='delete_word'),

    # WORD
    path('word/', views.word, name='word'),
    path('save_word/', views.saveWordProgress, name='save_word_progress'),

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