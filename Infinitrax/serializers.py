from rest_framework import serializers
from Infinitrax import models
from Infinitrax.models import Category
from Infinitrax.models import Brand
from Infinitrax.models import Attribute
from Infinitrax.models import Product
from Infinitrax.models import Inventory

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

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'                 