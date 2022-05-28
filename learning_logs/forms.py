from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        # класс Meta сообщает Django, на какой модели должна базироваться форма и какие поля на ней должны находиться.
        model = Topic               # форма создается на базе модели Topic
        fields = ['text']           # на ней размещается только поле text
        labels = {'text': ''}       # не генерировать подпись для текстового поля


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # widget - элемент формы HTML: однострочное или многострочное текстовое поле, раскрывающийся список и т. д.
        # Включая атрибут widgets, можем переопределить виджеты, выбранные Django по умолчанию.
        # Приказывая Django использовать элемент forms.Textarea, мы настраиваем виджет ввода для поля 'text',
        # чтобы ширина текстовой области составляла 80 столбцов вместо значения по умолчанию 40.
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
