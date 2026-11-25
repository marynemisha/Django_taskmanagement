from django.shortcuts import render
from django.db import models
from rest_framework import serializers
from rest_framework.views import APIView
from taskapp.serializers import UserSerializer,TaskSerializer
from taskapp.models import TaskDb
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
class Register(APIView):
    def post(self,request):
        serializer_instance=UserSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message":"User created successfully..!"
            })
        return Response({
            "Error":"Invalid data provided..!"
        })
class UserCreate(APIView):
    def get(self,request):
        user=User.objects.all()
        serializer_instance=UserSerializer(user,many=True)
        return Response(data=serializer_instance.data)
class TaskListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        task=TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(task,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        serializer_instance=TaskSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        return Response(data=serializer_instance.errors)

class TaskView(APIView):
    def get(self,request,id):
        try:
            data=TaskDb.objects.get(id=id,user=request.user)
            serializer_instance=TaskSerializer(data)
            return Response(data=serializer_instance.data)
        except TaskDb.DoesNotExist:
            return Response({
                "Message":"Task Not Found..!"
            })
    def put(self,request,id):
        try:
            data=TaskDb.objects.get(id=id,user=request.user)
            serializer_instance=TaskSerializer(data,data=request.data)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response(data=serializer_instance.data)
            return Response(data=serializer_instance.errors)
        except TaskDb.DoesNotExist:
            return Response(
                {
                    "Message":"Task Not Found..!"
                }
            )
    def delete(self,request,id):
        try:
            data=TaskDb.objects.get(id=id,user=request.user)
            data.delete()
            return Response({
                "Message":"Deleted...!"
            })
        except TaskDb.DoesNotExist:
            return Response({
                "Message":"Task Not Found...!"
            })