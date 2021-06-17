from django.contrib import admin

# Register your models here.
from .models import Book,User


class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title','author','description','category','publish_year']}),
        ('Borrowing details', {'fields': ['borrower','due_back','status']}),
    ]

admin.site.register(Book, BookAdmin)

admin.site.register(User)
