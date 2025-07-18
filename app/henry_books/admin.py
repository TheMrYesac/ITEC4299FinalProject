from django.contrib import admin
from .models import Book, Branch, Inventory

admin.site.register(Book)
admin.site.register(Branch)
admin.site.register(Inventory)