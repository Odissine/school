from django.contrib import admin
from import_export import resources, fields
from .models import LetterScore, WordOne, Halo, AdditionScore, WordScore, MultiplicationScore, SoustractionScore, AdditionPoseeScore
from import_export.admin import ImportMixin, ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from django.contrib.auth.models import Group


# RESOURCES
class LetterScoreResource(resources.ModelResource):
    class Meta:
        model = LetterScore


class AdditionScoreResource(resources.ModelResource):
    class Meta:
        model = AdditionScore


class MultiplicationScoreResource(resources.ModelResource):
    class Meta:
        model = MultiplicationScore


class AdditionPoseeScoreResource(resources.ModelResource):
    class Meta:
        model = AdditionPoseeScore


class SoustractionScoreResource(resources.ModelResource):
    class Meta:
        model = SoustractionScore


class WordScoreResource(resources.ModelResource):
    class Meta:
        model = WordScore


class WordOneResource(resources.ModelResource):
    groups = fields.Field(column_name='group', attribute='group', widget=ManyToManyWidget(Group, field='id'))

    class Meta:
        model = WordOne
        fields = ('id', 'name', 'slug', 'level', 'group')


class HaloResource(resources.ModelResource):
    class Meta:
        model = Halo


# ADMIN
class LetterScoreAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'score', 'level', 'user')
    resource_class = LetterScoreResource


class WordScoreAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'score', 'level', 'user')
    resource_class = WordScoreResource


class AdditionScoreAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'score', 'user')
    resource_class = AdditionScoreResource


class SoustractionScoreAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'score', 'user')
    resource_class = SoustractionScoreResource


class MultiplicationScoreAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'score', 'user')
    resource_class = MultiplicationScoreResource


class AdditionPoseeScoreAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'score', 'user')
    resource_class = AdditionPoseeScoreResource


class HaloAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'image')
    resource_class = HaloResource


class WordOneAdmin(ImportExportModelAdmin):
    ordering = ['id']
    list_display = ('id', 'name', 'slug', 'level', 'get_groups')
    resource_class = WordOneResource


admin.site.register(LetterScore, LetterScoreAdmin)
admin.site.register(WordScore, WordScoreAdmin)
admin.site.register(WordOne, WordOneAdmin)
admin.site.register(AdditionScore, AdditionScoreAdmin)
admin.site.register(SoustractionScore, SoustractionScoreAdmin)
admin.site.register(MultiplicationScore, MultiplicationScoreAdmin)
admin.site.register(AdditionPoseeScore, AdditionPoseeScoreAdmin)
admin.site.register(Halo, HaloAdmin)