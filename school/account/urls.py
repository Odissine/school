from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('preferences/', views.pref_view, name='preferences'),
    path('help/', views.help_view, name='help'),
    path('password_reset/', views.password_reset, name='password-reset'),
    path('success/', views.login_success, name='success'),
    path('user_list/<order>/', views.user_list, name='user-list'),
    path('export_users/', views.export_users, name='export-users'),
    path('export_user_excel/', views.export_user_excel, name='export-user-excel'),
    path('export_user_csv/', views.export_user_csv, name='export-user-csv'),
    path('change_password/', views.change_password, name='change-password'),
    path('forget/', views.lost_password, name='forget'),
    path('reset/<user>/<token>', views.reset_password, name='reset'),
    path('support/', views.support_view, name='support'),
]