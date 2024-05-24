from rest_framework.permissions import BasePermission
from API.models import Project, Contributor, Issues, Comments


class ProjectPermission(BasePermission):
    message = "Vous n'avez pas les droits pour effectuer cette action"

    def has_permission(self, request, view):
        # Donner l'accès à tous les utilisateurs authentifiés
        return bool(request.user and request.user.is_authenticated)
