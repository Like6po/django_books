from django.db import models


class Author(models.Model):
    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время регистрации", auto_now_add=True)
    first_name = models.CharField("Имя", max_length=128)
    second_name = models.CharField("Фамилия", max_length=128)


class Book(models.Model):
    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    name = models.CharField("Название", max_length=256)
    publish_date = models.DateField("Дата выпуска")
    archived = models.BooleanField("Архивировано", default=False)


class Comment(models.Model):
    id = models.AutoField("ID", primary_key=True)
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE, to_fields="id")
    book = models.ForeignKey(to="Book", on_delete=models.CASCADE, to_fields="id")

