from rest_framework.permissions import BasePermission
from API.models import Contributor, Issues, Comments


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


class IssuePermission(BasePermission):
    message = "Vous n'avez pas les droits pour effectuer cette action"

    def has_permission(self, request, view):
        # Donner l'accès à tous les utilisateurs authentifiés ET aux contributeurs du projet
        if request.method == "POST":
            return bool(request.user and request.user.is_authenticated and request.user.is_contributor)
        if request.method == "GET":
            return bool(request.user and request.user.is_authenticated)
