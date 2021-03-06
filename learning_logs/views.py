# learning_logs/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """Домашняя страница приложения Learning Log"""
    return render(request, 'learning_logs/index.html')


# Когда пользователь, не прошедший проверку, запрашивает страницу, защищенную декоратором @login_required,
# Django отправляет пользователя на URL-адрес, определяемый LOGIN_URL в settings.py
@login_required
def topics(request):
    """ Выводит список тем """
    # topics = Topic.objects.order_by('date_added')     # вывести ВСЕ темы
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  # вывести ТОЛЬКО ПРИНАДЛЕЖАЩИЕ пользователю темы
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
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
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # form.save()
            # Перенаправление пользователя к странице topics после отправки введенной темы
        # Функция reverse() определяет URL по заданной схеме URL(то есть Django сгенерирует URL при запросе страницы)
            # На этой странице пользователь видит только что введенную им тему в общем списке тем.
            return HttpResponseRedirect(reverse('learning_logs:topics'))
# Так как при создании TopicForm аргументы не передавались, Django создает пустую форму, которая заполняется пользователем.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)



# topic_id для сохранения полученного значения из URL.
# Идентификатор темы понадобится для отображения страницы и обработки данных формы,
# поэтому используем topic_id для получения правильного объекта темы
@login_required
def new_entry(request, topic_id):
    """ Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:  # теперь подставить ID чужой темы в URL не выйдет
        raise Http404
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        # Экземпляр EntryForm, заполненный данными POST из объекта запроса
        form = EntryForm(data=request.POST)

        if form.is_valid():
            # чтобы нельзя было добавить новую запись в журнал другого пользователя,
            # вводя URL-адрес с идентификатором темы, принадлежащей другому пользователю

            # аргумент commit=False для того, чтобы создать новый объект записи и сохранить его в new_entry,
            # не сохраняя пока в базе данных
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """ Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        # instance=entry этот аргумент приказывает Django создать форму, заранее заполненную информацией из
        # существующего объекта записи. Пользователь видит свои существующие данные и может отредактировать их.
        form = EntryForm(instance=entry)
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
