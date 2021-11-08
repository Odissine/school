from django.contrib import admin
from .models import LetterScore, Word, WordFind, Halo, AdditionScore

# LETTER
@admin.register(LetterScore)
class WordAdmin(admin.ModelAdmin):
    list_display = ['score', 'level', 'user']


# WORDS
@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'level', 'image', 'group']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(WordFind)
class WordFindAdmin(admin.ModelAdmin):
    list_display = ['word', 'user']


@admin.register(Halo)
class HaloAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']


# ADDITION
@admin.register(AdditionScore)
class AdditionScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'user']


admin.register(WordFind, WordFindAdmin, AdditionScore, Halo, LetterScore)
