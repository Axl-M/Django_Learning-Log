"""Определяет схемы URL для пользователей"""

from django.urls import re_path as url
# from django.contrib.auth.views import login
# from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    # страница входа
    # Схема страницы входа соответствует URL http://localhost:8000/users/login/ .
    # Когда Django читает этот URL-адрес, слово users указывает, что следует обратиться к users/urls.py,
    # а login сообщает о том, что запросы должны отправляться представлению login по умолчанию
    # url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login')
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # Страница регистрации
    # Шаблон соответствует URL http://localhost:8000/users/register/ и отправляет запросы функции register()
    url(r'^register/$', views.register, name='register'),
    # Страница выхода
    url(r'^logout/$', views.logout_view, name='logout'),
]

