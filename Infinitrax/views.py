from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from Infinitrax.serializers import CategorySerializer
from Infinitrax.models import Category

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
