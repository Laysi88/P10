from rest_framework import serializers
from CustomUser.models import CustomUser
from API.models import Project, Contributor


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["id", "user"]


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "start_date", "type", "author", "contributors"]
        read_only_fields = ["author"]  # Rendre le champ author en lecture seule

    def create(self, validated_data):
        # Capturer l'utilisateur actuel à partir de la requête HTTP
        user = self.context["request"].user
        # Ajouter l'utilisateur actuel comme auteur du projet
        validated_data["author"] = user
        # Créer le projet avec les données validées
        project = Project.objects.create(**validated_data)
        return project
