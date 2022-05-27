from django import forms
from .models import Topic


class TopicForm(forms.ModelForm):
    class Meta:
        # класс Meta сообщает Django, на какой модели должна базироваться форма и какие поля на ней должны находиться.
        model = Topic               # форма создается на базе модели Topic
        fields = ['text']           # на ней размещается только поле text
        labels = {'text': ''}       # не генерировать подпись для текстового поля
