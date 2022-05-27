"""Определяет схемы URL для learning_logs."""
# from django.conf.urls import re_path as url
from django.urls import re_path as url
from . import views

urlpatterns = [
    # Домашняя страница
    url(r'^$', views.index, name='index'),
    ]