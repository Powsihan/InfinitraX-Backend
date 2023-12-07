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