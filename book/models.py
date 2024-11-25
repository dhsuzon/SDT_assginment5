from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from .constants import  TRANSACTION_TYPES


class UserAccount(models.Model):
    user = models.OneToOneField(User,related_name="account",on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    
    def __str__(self):
       return f" UserFirstName: {self.user.first_name} - UserLastName: {self.user.last_name}" 
   
    
class CategoryModel(models.Model):
    categoryName = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)  
    
    def __str__(self):
        return self.categoryName
 


class BookModel(models.Model):
    image = models.ImageField(upload_to= 'book/uploads/')
    BookName = models.CharField(max_length=100)
    BookPrice = models.IntegerField(default=None)
    bookTitle = models.CharField(max_length=100)
    BookDescription = models.TextField()
    Category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    Status = models.CharField(max_length=20, default="available")
    def __str__(self):
        return  self.BookName
    

class BookTransactionHistory(models.Model):
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE,related_name="books")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bookuser")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)  
    is_returned = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} - {self.book.BookName} ({self.transaction_type})"
    
    
class UserComment(models.Model):
    comment = models.ForeignKey(BookModel,related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    email = models.EmailField()
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)