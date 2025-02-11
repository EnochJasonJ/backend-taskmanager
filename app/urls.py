from django.urls import path
from .views import list_tasks, create_tasks, update_tasks, delete_tasks, retrive_tasks, RegisterView, home_view, test_db, list_users
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("test-db/", test_db, name="test_db"),
    path("list-users/", list_users, name="list_users"),

    path("", list_tasks.as_view(), name="list_tasks"),  # Add this line
    path("list-tasks/", list_tasks.as_view(), name="list_tasks"),
    path("create-tasks/", create_tasks.as_view(), name="create_tasks"),
    path("update-tasks/<int:pk>/", update_tasks.as_view(), name="update_tasks"),
    path("delete-tasks/<int:pk>/", delete_tasks.as_view(), name="delete_tasks"),
    path("task/<int:pk>/", retrive_tasks.as_view(), name="retrieve_task"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
]
