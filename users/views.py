from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth import logout


def logout_view(request):
    """Завершает сеанс работы с приложением."""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))  # возврат к домашней странице
