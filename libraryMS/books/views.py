#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic
import datetime

from .models import Book,User

class IndexView(generic.ListView):
    template_name = 'books/index.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        search_query = self.request.GET.get('search_box', None)
        search_available = self.request.GET.get('available', None)

        if search_query==None and search_available==None:
            return Book.objects.order_by('id')

        if search_available:
            return Book.objects.filter(title__contains=search_query, status='Available')
        else:
            return Book.objects.filter(title__contains=search_query)


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'

    def users(self):
        return User.objects.all()

def returnB(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    selected_user = book.borrower
    book.status = "Available"
    book.due_back = None
    book.borrower = None
    book.save()
    selected_user.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('detail', args=(book.id,)))

def renew(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    book.due_back = book.due_back + datetime.timedelta(weeks = 1)
    book.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('detail', args=(book.id,)))

def borrow(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    try:
        userId = request.POST['dropdown']
        selected_user = User.objects.get(pk=userId)
        checkOverdue = Book.objects.filter(borrower=selected_user , due_back__lt = datetime.date.today())
        if selected_user.book_set.count()>=5:
            raise Exception(selected_user.user_name + " has borrow maximum number (5) of books")
        if checkOverdue:
            raise Exception(selected_user.user_name + " has overdue books")
    except (KeyError, User.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'books/detail.html', {
            'book': book,
            'users':User.objects.all(),
            'error_message': "You didn't select a user.",
        })
    except Exception as e:
        return render(request, 'books/detail.html', {
            'book': book,
            'users':User.objects.all(),
            'error_message': e,
        })
    else:
        book.status = "Not Available"
        book.due_back = datetime.date.today() + datetime.timedelta(weeks = 2)
        book.borrower = selected_user
        book.save()
        selected_user.total_books_borrowed = selected_user.total_books_borrowed + 1
        selected_user.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('detail', args=(book.id,)))
