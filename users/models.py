from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_librarian = models.BooleanField(default=False)
    is_memeber = models.BooleanField(default=False)
    username = models.CharField(max_length=100,null=True,blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
class Books(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default='available')
    
    def __str__(self):
        return self.name
        
class BooksManagement(models.Model):
    book = models.ForeignKey(Books,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=50,default='borrowed')
    
    