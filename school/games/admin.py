from django.contrib import admin
from .models import LetterScore, WordOne, Halo, AdditionScore, WordScore, MultiplicationScore, SoustractionScore, AdditionPoseeScore

# LETTER
@admin.register(LetterScore)
class LetterScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'level', 'user']


# WORDS
@admin.register(WordOne)
class WordOneFindAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'get_groups']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['level']
    ordering = ['name', 'level']

    def get_groups(self, obj):
        return ",".join([g.name for g in obj.group.all()])


@admin.register(WordScore)
class WordScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'level', 'user']


@admin.register(Halo)
class HaloAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']


# ADDITION
@admin.register(AdditionScore)
class AdditionScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'user']


# ADDITION POSEE
@admin.register(AdditionPoseeScore)
class AdditionPoseeScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'user']

# SOUSTRACTION
@admin.register(SoustractionScore)
class SoustractionScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'user']

# MULTIPLICATION
@admin.register(MultiplicationScore)
class MultiplicationScoreAdmin(admin.ModelAdmin):
    list_display = ['score', 'user']

admin.register(AdditionScore, MultiplicationScore, SoustractionScore, AdditionPoseeScore, LetterScore, WordOne, WordScore)
