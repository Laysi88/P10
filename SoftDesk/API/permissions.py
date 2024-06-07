from rest_framework.permissions import BasePermission
from API.models import Contributor, Issues, Comments, Project
from django.shortcuts import get_object_or_404


class ProjectPermission(BasePermission):
    message = "Vous n'avez pas les droits pour effectuer cette action"

    def has_permission(self, request, view):
        # Donner l'accès à tous les utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        elif request.method == "GET":
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "POST":
            return True
        else:
            return False


class IssuePermissionCreate(BasePermission):
    message = "Vous n'avez pas les droits pour effectuer cette action"

    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs.get("pk"))

        if request.user and request.user.is_authenticated:
            return request.user == project.author or project.contributors.filter(id=request.user.id).exists()
        return False


class IssuePermissionUpdate(BasePermission):
    message = "Vous n'avez pas les droits pour effectuer cette action"

    def has_object_permission(self, request, view, obj):
        issue = get_object_or_404(Issues, id=view.kwargs.get("pk"))
        if request.method == "GET":
            if request.user and request.user.is_authenticated:
                return request.user == issue.author or issue.assigned.user == request.user
        if request.method == "PUT" or request.method == "DELETE":
            return bool(obj.author == request.user)
        else:
            return False
