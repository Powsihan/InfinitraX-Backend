from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from Infinitrax.serializers import CategorySerializer
from Infinitrax.models import Category
from Infinitrax.serializers import BrandSerializer
from Infinitrax.models import Brand
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from knox.auth import AuthToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

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
