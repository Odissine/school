from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('password-reset/', views.password_reset, name='password-reset'),
    path('success/', views.login_success, name='success'),
    path('user_list/<order>/', views.user_list, name='user-list'),
    path('export_users/', views.export_users, name='export-users'),
    path('export_user_excel/', views.export_user_excel, name='export-user-excel'),
    path('change_password/', views.change_password, name='change-password'),
]