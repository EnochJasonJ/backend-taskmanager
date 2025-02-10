from django.urls import path
from .views import list_tasks, create_tasks, update_tasks, delete_tasks, retrive_tasks, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('list-tasks/', list_tasks.as_view(), name='list_tasks'),
    path('create-tasks/', create_tasks.as_view(), name='create_tasks'),
    path('update-tasks/<int:pk>/', update_tasks.as_view(), name='update_tasks'),
    path('delete-tasks/<int:pk>/', delete_tasks.as_view(), name='delete_tasks'),
    path('task/<int:pk>/', retrive_tasks.as_view(), name='retrieve_task'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
