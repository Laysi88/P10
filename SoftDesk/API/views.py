from rest_framework import viewsets
from .models import Project, Contributor, Issues, Comments
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssuesSerializerCreate,
    IssuesSerializerUpdate,
    CommentsSerializerCreate,
    CommentsSerializerUpdate,
)

from API.permissions import (
    ProjectPermission,
    IssuePermissionCreate,
    IssuePermissionUpdate,
    CommentPermissionCreate,
    CommentPermissionUpdate,
)
from rest_framework.response import Response
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Projet supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


class IssuesCreateViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializerCreate
    permission_classes = [IssuePermissionCreate]

    def get_queryset(self):
        project_id = self.kwargs.get("pk")
        return Issues.objects.filter(project_id=project_id)


class IssuesUpdateViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializerUpdate
    permission_classes = [IssuePermissionUpdate]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Issue supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CommentsCreateViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializerCreate
    permission_classes = [CommentPermissionCreate]

    def get_queryset(self):
        issue_id = self.kwargs.get("pk")
        return Comments.objects.filter(issue_id=issue_id)


class CommentsUpdateViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializerUpdate
    permission_classes = [CommentPermissionUpdate]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Commentaire supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
