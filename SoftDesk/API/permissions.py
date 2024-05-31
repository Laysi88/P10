from rest_framework.permissions import BasePermission
from API.models import Contributor, Issues, Comments, Project


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
        try:
            project = Project.objects.get(id=view.kwargs.get("pk"))
        except Project.DoesNotExist:
            return False

        contributors = project.contributors.all()

        if request.user and request.user.is_authenticated:
            for contributor in contributors:
                if request.user.id == contributor.user.id or project.author.id == request.user.id:
                    return True
        return False
