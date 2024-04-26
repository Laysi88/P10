from rest_framework import viewsets
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save()
        # Vérification de l'existence d'un Contributor pour l'utilisateur actuel
        contributor, created = Contributor.objects.get_or_create(user=self.request.user)
        # Ajout du nouveau projet aux contributeurs existants
        if not serializer.instance in contributor.project.all():
            contributor.project.add(serializer.instance)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
