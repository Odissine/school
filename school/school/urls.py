"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin DJANGO
    path('admin/', admin.site.urls),
    path("select2/", include("django_select2.urls")),

    # Index du site
    path('', include(('main.urls', 'main'), namespace='main')),
    # path('', include("django.contrib.auth.urls")),

    path('i18n/', include('django.conf.urls.i18n')),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('quiz/', include(('poll.urls', 'quiz'), namespace='quiz')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)