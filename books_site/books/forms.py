from django import forms

from books.models import Author


class CommentForm(forms.Form):
    comment = forms.CharField(label="Комментарий", max_length=4096)


class BookForm(forms.Form):
    name = forms.CharField(label="Название книги")
    publish_date = forms.DateField(label="Дата выпуска")
    archived = forms.BooleanField(label="Архивировано?", required=False)
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.all(), label="Авторы")
