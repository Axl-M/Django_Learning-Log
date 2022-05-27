from django.shortcuts import render
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.urls import reverse
from .models import Topic
from .forms import TopicForm


# Create your views here.
def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """ Выводит список тем """
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':    # запросил ли пользователь пустую форму (запрос GET)
        # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        # Обработать заполненную форму (запрос POST).
        # Отправлены данные POST; обработать данные.
        form = TopicForm(request.POST)
        # Отправленную информацию нельзя сохранять в базе данных пока она не будет проверена
        if form.is_valid():
            form.save()
            # Перенаправление пользователя к странице topics после отправки введенной темы
        # Функция reverse() определяет URL по заданной схеме URL(то есть Django сгенерирует URL при запросе страницы)
            # На этой странице пользователь видит только что введенную им тему в общем списке тем.
            return HttpResponseRedirect(reverse('learning_logs:topics'))
# Так как при создании TopicForm аргументы не передавались, Django создает пустую форму, которая заполняется пользователем.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
