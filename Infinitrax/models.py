from django.db import models


class Category(models.Model):
    categories = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

        
