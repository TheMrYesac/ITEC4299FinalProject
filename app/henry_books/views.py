from django.shortcuts import get_object_or_404, render
from.models import Book, Branch, Inventory

def book_list(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'henry_books/book_list.html', context)

def branch_list(request):
    branches = Branch.objects.all()
    context = {'branches': branches}
    return render(request, 'henry_books/branch_list.html', context)

def inventory_list(request):
    inventory = Inventory.objects.all()
    context = {'inventory': inventory}
    return render(request, 'henry_books/inventory_list.html', context)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {'book': book}
    return render(request, 'henry_books/book_detail.html', context)