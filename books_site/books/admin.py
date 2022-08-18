from django.contrib import admin

from books.models import Author, Book, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "get_books_count", "get_comments_count"]

    def get_books_count(self, obj):
        return Book.objects.filter(authors=obj.id).count()

    get_books_count.short_description = "Количество книг"

    def get_comments_count(self, obj):
        return Comment.objects.filter(author=obj.id).count()

    get_comments_count.short_description = "Количество комментариев"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "publish_date", "get_authors", "get_comments_count"]

    def get_authors(self, obj):
        return ", ".join([p.first_name for p in obj.authors.all()])

    get_authors.short_description = "Авторы"

    def get_comments_count(self, obj):
        return Comment.objects.filter(book=obj.id).count()

    get_comments_count.short_description = "Количество комментариев"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
