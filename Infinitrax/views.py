from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from Infinitrax.serializers import CategorySerializer
from Infinitrax.models import Category
from Infinitrax.serializers import BrandSerializer
from Infinitrax.models import Brand

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
