from django.shortcuts import render

from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Task,Category
from .serializers import TaskSerializer,CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):

    #serializer is basically a translator and view is the managers or cook who does all the work
    #This is used to connect the TaskViewSet with TaskSerializer means views with serializer
    #think it like this when user will input some data it will go to view and view will
    # send it to serializer to validate and to and convert it and then it will go to 
    # model and get saved in database 
    serializer_class = TaskSerializer

    #we use permission here because user cannot access this without login it means login required
    #without login 401 unauthorized will get
    permission_classes = [IsAuthenticated]

    

    #This is a search engine
    # filter_backends give us the tools for searching like search filter or more 
    filter_backends=[
        DjangoFilterBackend, #it enables precise filtering based on filed values,it relies on filterset_fields
        filters.SearchFilter,#it enables text-based searching across multiple fields
        filters.OrderingFilter #enable sorting the result by specific fields 
    ]
    filterset_fields = ['status','priority','category']#it is connect to djangofilelterbackend , user can only filter using those fields
    search_fields = ['title','description','tags']#defines which text fields the search bar should look into
    ordering_fields = ['created_at','due_date','priority'] #it basically used for soring purpose only these field are allowed to sort mean ascending and descending of data
    ordering = ['-created_at']#its default sorted to newest first mean descending  if user doesn't specify one 

    #we have used this for data insolation so only user can see only user data not other
    #user data
    def get_queryset(self):
        return Task.objects.filter( #this line is used for filter
            user = self.request.user#this line tell that it can see  task from current login in user only 

        ).select_related('category')#this is for performance optimization still don't have much info on it
    

    def perform_create(self,serializer): #this runs automatically when data is validated but before data is saved in database
        serializer.save(user= self.request.user)#this means only save the data when the user is current login user so it prevent fraud 

    #We use action decorator when we want to create custom endpoint like /tasks/{id}/complete/
    @action(
        detail = True,#it means take single task like /tasks/{id}/complete/
        method = ['POST'],#only post request
        url_path = 'complete',#its the url path then it becomes /tasks/{id}/complete/
    )
    def complete(self,request,pk=None):
        

# Create your views here.

