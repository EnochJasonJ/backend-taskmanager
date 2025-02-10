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

