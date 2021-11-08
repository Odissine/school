from django.contrib import admin
from django.contrib.auth.models import User


class MyUserAdmin(admin.ModelAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_superuser', 'last_login', 'group']
    list_filter = ['groups',]

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)