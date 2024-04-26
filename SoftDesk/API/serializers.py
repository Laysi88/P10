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

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)

        return project
