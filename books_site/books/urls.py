from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('books/', views.all_books, name='books'),
    path("book/<int:book_id>/", views.detail_book, name="books-detail"),
    path("authors/", views.all_authors, name="authors"),
    path("author/<int:author_id>/", views.detail_author, name="authors-detail"),
    path("author/<int:author_id>/books", views.author_books, name="author-books"),
    path("book/<int:book_id>/comment", views.post_comment_to_book, name="post_comment_to_book"),
    path("book/<int:book_id>/edit", views.edit_book, name="edit_book"),
    path("book/<int:book_id>/delete", views.delete_book, name="delete_book"),
    path("book/<int:book_id>/comment/<comment_id>/delete", views.delete_comment, name="delete_comment"),
    path("book/<int:book_id>/comment/<comment_id>/edit", views.edit_comment, name="edit_comment"),
]
