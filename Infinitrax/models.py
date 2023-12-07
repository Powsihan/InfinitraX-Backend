from django.db import models

class User():
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Category(models.Model):
    categories = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    
class Brand(models.Model):
    brand = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

class Attribute(models.Model):
    attribute = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class Product(models.Model):
    serialno = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField()

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, to_field='serialno')
    attribute = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    price = models.IntegerField()
    inventory = models.IntegerField()
    taxrate = models.CharField(max_length=255)
