from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from Infinitrax.serializers import CategorySerializer
from Infinitrax.models import Category
from Infinitrax.serializers import BrandSerializer
from Infinitrax.models import Brand
from Infinitrax.models import Attribute
from Infinitrax.serializers import AttributeSerializer
from Infinitrax.serializers import ProductSerializer
from Infinitrax.models import Product
from Infinitrax.serializers import InventorySerializer
from Infinitrax.models import Inventory
from Infinitrax.models import User
from Infinitrax.serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import AuthenticationFailed
from knox.auth import AuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from knox.auth import AuthToken, TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist


@api_view(['POST'])
def login_user(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        user = get_user_model().objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        _, token = AuthToken.objects.create(user)
        user.is_active = True
        user.save()
        return Response({
            'user_info': {
                'username': user.username,
                'password': user.password
            },
            'token': token
        }, status=status.HTTP_200_OK)
    except KeyError:
        return Response({
            "details": "error"
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_user(request):
    try:
        return Response({
            "details": "Token is valid"
        }, status=status.HTTP_200_OK)
    except KeyError:
        return Response({
            "details": "Token is invalid"
        }, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def categoryApi(request,id=0):
    if request.method=='GET':
        category = Category.objects.all()
        category_serializer=CategorySerializer(category,many=True)
        return JsonResponse(category_serializer.data,safe=False)
    elif request.method=='POST':
        category_data=JSONParser().parse(request)
        category_serializer=CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        category_data=JSONParser().parse(request)
        category=Category.objects.get(id=id)
        category_serializer=CategorySerializer(category,data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        category=Category.objects.get(id=id)
        category.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def brandApi(request,id=0):
    if request.method=='GET':
        brand = Brand.objects.all()
        brand_serializer=BrandSerializer(brand,many=True)
        return JsonResponse(brand_serializer.data,safe=False)
    elif request.method=='POST':
        brand_data=JSONParser().parse(request)
        brand_serializer=BrandSerializer(data=brand_data)
        if brand_serializer.is_valid():
            brand_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        brand_data=JSONParser().parse(request)
        brand=Brand.objects.get(id=id)
        brand_serializer=BrandSerializer(brand,data=brand_data)
        if brand_serializer.is_valid():
            brand_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        brand=Brand.objects.get(id=id)
        brand.delete()
        return JsonResponse("Deleted Successfully",safe=False)

@csrf_exempt
def attributeApi(request,id=0):
    if request.method=='GET':
        attribute = Attribute.objects.all()
        attribute_serializer=AttributeSerializer(attribute,many=True)
        return JsonResponse(attribute_serializer.data,safe=False)
    elif request.method=='POST':
        attribute_data=JSONParser().parse(request)
        attribute_serializer=AttributeSerializer(data=attribute_data)
        if attribute_serializer.is_valid():
            attribute_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        attribute_data=JSONParser().parse(request)
        attribute=Attribute.objects.get(id=id)
        attribute_serializer=AttributeSerializer(attribute,data=attribute_data)
        if attribute_serializer.is_valid():
            attribute_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        attribute=Attribute.objects.get(id=id)
        attribute.delete()
        return JsonResponse("Deleted Successfully",safe=False)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def get_user(request):
    try:
        user = request.user
        user_data = {
            'username': user.username,
            'email': user.email,
        }
        return Response(user_data)

    except User.DoesNotExist:
        return Response({
            "error": "User not found"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "error": "An error occurred"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


       

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@csrf_exempt
def productApi(request, id=0):
    if request.method == 'GET':
        if id:
            try:
                product = Product.objects.get(id=id)
                product_serializer = ProductSerializer(product)
                inventory = Inventory.objects.filter(product=product.serialno)
                inventory_serializer = InventorySerializer(inventory, many=True)
                response_data = {
                    'product': product_serializer.data,
                    'inventory': inventory_serializer.data
                }
                return Response(response_data)
            except Product.DoesNotExist:
                return Response({'message': 'Product not found'}, status=404)

        else:
            products = Product.objects.all()
            product_serializer = ProductSerializer(products, many=True)
            inventory = Inventory.objects.all()
            inventory_serializer = InventorySerializer(inventory, many=True)
            response_data = {
                'products': product_serializer.data,
                'inventory': inventory_serializer.data
            }
            return Response(response_data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=data)

        if product_serializer.is_valid():
            product = product_serializer.save()

            if 'inventory' in data and isinstance(data['inventory'], list):
                inventory_data_list = data['inventory']
                for inventory_data in inventory_data_list:
                    inventory_data['product'] = product.serialno  
                    inventory_serializer = InventorySerializer(data=inventory_data)

                    if inventory_serializer.is_valid():
                        inventory_serializer.save()
                    else:
                        product.delete() 
                        return JsonResponse(inventory_serializer.errors, status=400)

                return JsonResponse("Product and Inventory Added Successfully", safe=False)

            return JsonResponse("Product Added Successfully", safe=False)

        return JsonResponse(product_serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)

        data = JSONParser().parse(request)
        product_serializer = ProductSerializer(product, data=data)

        if product_serializer.is_valid():
            product_serializer.save()

            if 'inventory' in data:
                inventory_data_list = data['inventory']

                for inventory_data in inventory_data_list:
                    inventory = Inventory.objects.get(id=inventory_data.get('id'))

                    inventory_serializer = InventorySerializer(inventory, data=inventory_data)

                    if inventory_serializer.is_valid():
                        inventory_serializer.save()
                    else:
                        return JsonResponse(inventory_serializer.errors, status=400)

                return JsonResponse("Product and Inventory Updated Successfully", safe=False)
                
            return JsonResponse("Product Updated Successfully", safe=False)

        return JsonResponse(product_serializer.errors, status=400)
     
    elif request.method == 'DELETE':
        try:
            product = Product.objects.get(id=id)
            Inventory.objects.filter(product=product.serialno).delete()
            product.delete()  
            return JsonResponse("Product and associated inventory deleted successfully", safe=False)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found'}, status=404)
 
 
@api_view(['POST'])
def AddInventoryApi(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if 'serialno' not in data:
            return JsonResponse({'error': 'Serialno is required to add inventory'}, status=400)
        try:
            product = Product.objects.get(serialno=data['serialno'])
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product with the provided serialno does not exist'}, status=400)
        if 'inventory' in data and isinstance(data['inventory'], list):
            inventory_data_list = data['inventory']
            for inventory_data in inventory_data_list:
                if isinstance(inventory_data, dict):
                    inventory_data['product'] = product.serialno
                    inventory_serializer = InventorySerializer(data=inventory_data)

                    if inventory_serializer.is_valid():
                        inventory_serializer.save()
                    else:
                        return JsonResponse(inventory_serializer.errors, status=400)
                else:
                    return JsonResponse({'error': 'Invalid format for inventory_data'}, status=400)

            return JsonResponse("Inventory Added Successfully", safe=False)

        return JsonResponse("No valid inventory data provided", status=400)



