import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect

from .forms import CommentForm, BookForm
from .models import Book, Author, Comment


def index(request: WSGIRequest):
    return render(request, "books/index.html")


def all_books(request: WSGIRequest):
    books_list = Book.objects.filter(archived=False)
    return render(request, 'books/all_books.html', {'books_list': books_list})


def detail_book(request: WSGIRequest, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    book_comments_list = Comment.objects.filter(book=book_id)

    return render(request, 'books/detail_book.html',
                  {'book': book, 'comments': book_comments_list, "form": CommentForm})


def all_authors(request: WSGIRequest):
    authors_list = Author.objects.all()
    return render(request, "books/all_authors.html", {"authors_list": authors_list})


def detail_author(request: WSGIRequest, author_id: int):
    try:
        author = Author.objects.get(id=author_id)
    except Book.DoesNotExist:
        raise Http404("Author does not exist")
    return render(request, 'books/detail_author.html', {'author': author})


def author_books(request: WSGIRequest, author_id: int):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        raise Http404("Author does not exist")

    books_list = Book.objects.filter(authors=author_id)

    return render(request, 'books/author_books.html', {'author': author, 'books_list': books_list})


def post_comment_to_book(request: WSGIRequest, book_id: int):
    if not request.POST:
        raise HttpResponseBadRequest()
    if not CommentForm(request.POST).is_valid():
        raise HttpResponseBadRequest()

    Comment.objects.create(author=Author.objects.get(id=Author.objects.all()[0].id), book=Book.objects.get(id=book_id),
                           text=request.POST["comment"])
    return redirect(f"/book/{book_id}")


def edit_book(request: WSGIRequest, book_id: int):
    if not request.POST:
        book = Book.objects.get(id=book_id)
        return render(request, 'books/edit_book.html',
                      {"form": BookForm({"name": book.name,
                                         "publish_date": book.publish_date,
                                         "archived": book.archived,
                                         "authors": book.authors.all()})})
    form = BookForm(request.POST)

    if not form.is_valid():
        raise HttpResponseBadRequest()

    authors_update: QuerySet = form.data.getlist("authors")
    Book.objects.filter(id=book_id).update(name=form.cleaned_data.get("name"),
                                           archived=form.cleaned_data.get("archived"),
                                           publish_date=datetime.datetime.strptime(
                                               form.data.get("publish_date"),
                                               "%d.%m.%Y"))
    authors_actual = Author.objects.filter(book=book_id)
    current_book: QuerySet = Book.objects.get(id=book_id)
    for author in authors_actual:
        if author.id not in authors_update:
            current_book.authors.remove(author.id)
    for author_id in authors_update:
        if author_id not in [author.id for author in authors_actual]:
            current_book.authors.add(author_id)
    return redirect(f"/book/{book_id}")


def delete_book(request: WSGIRequest, book_id: int):
    Book.objects.get(id=book_id).delete()
    return redirect(f"/books")


def delete_comment(request: WSGIRequest, book_id, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect(f"/book/{book_id}")


def edit_comment(request: WSGIRequest, book_id, comment_id):
    if not request.POST:
        comment = Comment.objects.get(id=comment_id)
        return render(request, 'books/edit_comment.html',
                      {"form": CommentForm({"comment": comment.text})})

    form = CommentForm(request.POST)

    if not form.is_valid():
        raise HttpResponseBadRequest()
    Comment.objects.filter(id=comment_id).update(text=form.cleaned_data.get("comment"))

    return redirect(f"/book/{book_id}")
