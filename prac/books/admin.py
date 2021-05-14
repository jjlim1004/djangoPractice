from django.contrib import admin

# Register your models here.
from books.models import Publisher, Author, Book

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)