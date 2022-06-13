from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    """Тема, которую изучает пользователь"""
    # то есть заголовок
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)     # связываем ТЕМУ и ПОЛЬЗОВАТЕЛЯ

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text


class Entry(models.Model):
    """Информация, изученная пользователем по теме"""
    # текст, который будет ассоциирован с одной из тем
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Возвращает строковое представление модели."""
        if len(self.text) < 50:
            return self.text
        else:
            return self.text[:50] + "..."
