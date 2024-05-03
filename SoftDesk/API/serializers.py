from rest_framework import serializers
from CustomUser.models import CustomUser
from API.models import Project, Contributor, Issues, Comments
from CustomUser.models import CustomUser


class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "user", "project"]


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())
    author = serializers.StringRelatedField()

    class Meta:
        model = Project
        fields = ["id", "name", "description", "start_date", "type", "author", "contributors"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        # Capturer l'utilisateur actuel à partir de la requête HTTP
        user = self.context["request"].user
        # Ajouter l'utilisateur actuel comme auteur du projet
        validated_data["author"] = user
        # Récupérer les contributeurs fournis dans les données validées
        contributors_data = validated_data.pop("contributors", [])
        # Créer le projet avec les données validées
        project = Project.objects.create(**validated_data)
        # Ajouter l'auteur en tant que contributeur du projet s'il n'existe pas déjà
        author_contributor, created = Contributor.objects.get_or_create(user=user)
        author_contributor.project.add(project)
        # Ajouter des contributeurs au projet s'ils sont fournis
        for contributor_data in contributors_data:
            # Récupérer ou créer l'utilisateur à partir des données du contributeur
            contributor_user, created = CustomUser.objects.get_or_create(username=contributor_data.username)
            # Récupérer ou créer le Contributor associé à l'utilisateur
            contributor, created = Contributor.objects.get_or_create(user=contributor_user)
            # Ajouter le projet au Contributor
            contributor.project.add(project)
        return project

    def update(self, instance, validated_data):
        # Vérification que l'utilisateur actuel est l'auteur du projet
        if self.context["request"].user == instance.author:
            # Mettre à jour le projet avec les données validées
            instance.name = validated_data.get("name", instance.name)
            instance.description = validated_data.get("description", instance.description)
            instance.type = validated_data.get("type", instance.type)
            # Récupérer les contributeurs fournis dans les données validées
            contributors_data = validated_data.pop("contributors", [])
            # Ajouter des contributeurs au projet s'ils sont fournis
            for contributor_data in contributors_data:
                # Récupérer ou créer l'utilisateur à partir des données du contributeur
                contributor_user, created = CustomUser.objects.get_or_create(username=contributor_data.username)
                # Récupérer ou créer le Contributor associé à l'utilisateur
                contributor, created = Contributor.objects.get_or_create(user=contributor_user)
                # Ajouter le projet au Contributor
                contributor.project.add(instance)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError("Vous n'êtes pas autorisé à modifier ce projet.")


class IssuesSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Issues
        fields = [
            "id",
            "project",
            "title",
            "description",
            "start_date",
            "author",
            "assigned",
            "priority",
            "nature",
            "status",
        ]
        read_only_fields = ["author"]

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user
        project_id = self.context["view"].kwargs.get("pk")
        if user.is_authenticated:
            project = Project.objects.get(id=project_id)
            contributors = project.contributors.all()
            fields["assigned"].queryset = contributors
            fields["project"].queryset = Project.objects.filter(id=project_id)
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        return super().create(validated_data)
