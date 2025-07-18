from django.db import models

"""
Records info about the books being sold
"""
class Book(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null= True)
    thumbnail_url = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    
"""
Records info about branches of the bookstore
"""
class Branch(models.Model):
    branch_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.branch_name
    
    
"""
Records info about inventory of each branch
Book and Branch are foreign keys    
"""
class Inventory(models.Model):
    # If a book is deleted, inventory records also go
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    # If a branch is deleted, inventory records also go
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    # Default quantity to zero
    quantity = models.IntegerField(default=0)
    
    class Meta:
        # Cannot put same book twice per branch
        unique_together = (('book', 'branch'),)
        
        # Fix Django default pluralization
        verbose_name_plural = "Inventories"
        
    def __str__(self):
        return f"{self.quantity} of {self.book.title} at {self.branch.branch_name}"