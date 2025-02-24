from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView , DestroyAPIView, RetrieveAPIView
from .serializers import TaskSerializer
from .models import TaskModel
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.management import call_command

from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model

from django.db import connection


def run_migrations(request):
    try:
        call_command("migrate")
        return JsonResponse({"message": "Migrations applied successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

def test_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")  # Simple DB check
        return JsonResponse({"status": "Database is connected!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def list_users(request):
    users = list(User.objects.values("username"))
    return JsonResponse({"users": users})


class TaskAnalyticsView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        total_tasks = TaskModel.objects.filter(user=request.user).count()
        completed_tasks = TaskModel.objects.filter(user=request.user, is_completed=True).count()
        not_completed_tasks = total_tasks - completed_tasks
        completion_percentage = 0 if total_tasks == 0 else (completed_tasks / total_tasks) * 100

        return Response({
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "not_completed_tasks": not_completed_tasks,
            "completion_percentage": completion_percentage
        })

def home_view(request):
    return JsonResponse({"message": "Backend is running!"})

# Create your views here.

class list_tasks(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class create_tasks(CreateAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class retrive_tasks(RetrieveAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    lookup_field= 'pk'
    permission_classes = [IsAuthenticated]

class update_tasks(UpdateAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return get_object_or_404(TaskModel, pk=self.kwargs['pk'], user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class delete_tasks(DestroyAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(TaskModel, pk=self.kwargs['pk'], user=self.request.user)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'message': 'User registered successfully',
                "refresh": str(refresh),
                "access": str(refresh.access_token)
                }, status=status.HTTP_201_CREATED)

