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
from rest_framework.response import Response
from rest_framework import status
from API.permissions import ProjectPermission, IssuePermissionCreate


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermission]


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


class CommentsCreateViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializerCreate

    def get_queryset(self):
        issue_id = self.kwargs.get("pk")
        return Comments.objects.filter(issue_id=issue_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentsUpdateViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializerUpdate
