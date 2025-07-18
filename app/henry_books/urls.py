from django.urls import path
from . import views

urlpatterns = [
    # Path for listing all books
    path('books/', views.book_list, name='book_list'),
    
    # Path for a specific book's details
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
]
