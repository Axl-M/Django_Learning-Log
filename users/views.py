""" users/views.py """
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """Завершает сеанс работы с приложением."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))  # возврат к домашней странице


def register(request):
    """Регистрирует нового пользователя."""
    if request.method != 'POST':
        # Отобразить пустую форму для регистрации.
        form = UserCreationForm()
    else:
        # Обработка заполненной формы.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Выполнение входа и перенаправление на домашнюю страницу.
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            # Используем password1. Но можно использовать и 2-й т.к. при регистрации они должны совпадать
            login(request, authenticated_user)  # создает действительный сеанс для нового пользователя.
            return HttpResponseRedirect(reverse('learning_logs:index'))  # перенаправляем на домашнюю страницу
    context = {'form': form}
    return render(request, 'users/register.html', context)
