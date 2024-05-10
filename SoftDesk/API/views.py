from rest_framework import viewsets
from .models import Project, Contributor, Issues
from .serializers import ProjectSerializer, ContributorSerializer, IssuesSerializerCreate, IssuesSerializerUpdate
from rest_framework.response import Response
from rest_framework import status


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer


class IssuesCreateViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializerCreate

    def get_queryset(self):
        project_id = self.kwargs.get("pk")
        return Issues.objects.filter(project_id=project_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class IssuesUpdateViewSet(viewsets.ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializerUpdate
