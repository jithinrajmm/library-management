from django.contrib import admin
from users.models import User,Books,BooksManagement

models = [User,Books,BooksManagement]
admin.site.register(models)

# Register your models here.
