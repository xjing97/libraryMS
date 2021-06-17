from django.db import models
from datetime import date

USER_GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200)
    age = models.IntegerField(default="")
    gender = models.CharField(
        max_length=10,
        choices=USER_GENDER,
        default='')
    total_books_borrowed = models.IntegerField(default=0)

    db_table='books_user'

    def __str__(self):
        """String for representing the Model object."""
        return '{0}. {1}'.format(self.id, self.user_name)

#using Dewey Decimal System
BOOK_CATEGORY =(
    ('000','Computer science, information and general works'),
    ('100','Philosophy and psychology'),
    ('200','Religion'),
    ('300','Social Sciences'),
    ('400','Language'),
    ('500','Science'),
    ('600','Technology and applied science'),
    ('700','Arts and recreation'),
    ('800','Literature'),
    ('900','History and geography')
)

BOOK_STATUS = (
    ('Available','Available'),
    ('Not Available','Not Available')
)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    category = models.CharField(max_length=200,choices=BOOK_CATEGORY)
    publish_year = models.IntegerField()
    borrower = models.ForeignKey(User, default="",on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=200,choices=BOOK_STATUS,default="Available")

    db_table='books_book'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return (date.today() - self.due_back).days
        return 0


    def __str__(self):
        """String for representing the Model object."""
        return '{0}. {1} ({2}) - {3}'.format(self.id, self.title, self.publish_year, self.status)
