from rest_framework import serializers
from Infinitrax import models
from Infinitrax.models import Category
from Infinitrax.models import Brand

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password']

        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'