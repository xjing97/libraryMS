from django.urls import path

from . import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/status/', views.StatusView.as_view(), name='status'),
    path('<int:book_id>/returnB/', views.returnB, name='returnB'),
    path('<int:book_id>/renew/', views.renew, name='renew'),
    path('<int:book_id>/borrow/', views.borrow, name='borrow'),

    #path('<int:book_id>/status/', views.status, name='status'),
    #path('<int:book_id>/returnB/', views.returnB, name='returnB'),
    #path('<int:book_id>/borrow/', views.borrow, name='borrow'),
]
