from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export import resources, fields
from import_export.admin import ImportMixin, ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget


class MyUserAdmin(admin.ModelAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'last_login', 'group']
    list_filter = ['groups',]


# RESOURCES
class UserResource(resources.ModelResource):
    groups = fields.Field(column_name='groups', attribute='groups', widget=ManyToManyWidget(Group, field='id'))

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups')


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group
        fields = ('id', 'name')


# ADMIN
class UserAdmin(ImportExportModelAdmin):
    ordering = ['last_name', 'first_name']
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
    resource_class = UserResource


class GroupAdmin(ImportExportModelAdmin):
    ordering = ['name']
    list_display = ('name',)
    resource_class = GroupResource


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
