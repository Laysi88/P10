"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from CustomUser.views import CustomUserCreate, CustomUserUpdate, CustomUserDelete
from API.views import (
    ProjectViewSet,
    ContributorViewSet,
    IssuesCreateViewSet,
    IssuesUpdateViewSet,
    CommentsCreateViewSet,
    CommentsUpdateViewSet,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# API URL
router = routers.DefaultRouter()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/users/", CustomUserCreate.as_view(), name="user_create"),
    path("api/users/me/", CustomUserUpdate.as_view(), name="user_update"),
    path("api/users/me/delete/", CustomUserDelete.as_view(), name="user_delete"),
    path("api/projects/", ProjectViewSet.as_view({"get": "list", "post": "create"}), name="project_list"),
    path(
        "api/projects/<int:pk>/",
        ProjectViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="project_detail",
    ),
    path("api/contributors/", ContributorViewSet.as_view({"get": "list", "post": "create"}), name="contributor_list"),
    path(
        "api/projects/<int:pk>/issues/",
        IssuesCreateViewSet.as_view({"get": "list", "post": "create"}),
        name="issues",
    ),
    path(
        "api/issues/<int:pk>/",
        IssuesUpdateViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="issues_detail",
    ),
    path(
        "api/issues/<int:pk>/comments/",
        CommentsCreateViewSet.as_view({"get": "list", "post": "create"}),
        name="comments",
    ),
    path(
        "api/comments/<int:pk>/",
        CommentsUpdateViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="comments_detail",
    ),
]
