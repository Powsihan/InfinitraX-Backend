from django.db import models

class User():
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)

class Category(models.Model):
    categories = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    
class Brand(models.Model):
    brand = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
        
