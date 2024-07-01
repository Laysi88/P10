from rest_framework import serializers
from CustomUser.models import CustomUser
from API.models import Project, Contributor, Issues, Comments
from CustomUser.models import CustomUser
from django.shortcuts import get_object_or_404


class ContributorSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.CharField()

    class Meta:
        model = Contributor
        fields = ["id", "user", "project", "user_id"]

    def validate_user(self, value):
        """Valide et convertit le nom d'utilisateur en une instance d'utilisateur."""
        try:
            user = CustomUser.objects.get(username=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Utilisateur avec ce nom d'utilisateur n'existe pas.")
        return user

    def create(self, validated_data):
        """Crée un contributeur avec l'utilisateur validé."""
        user = validated_data.pop("user")
        contributor = Contributor.objects.create(user=user, **validated_data)
        return contributor


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "start_date", "type", "author", "contributors"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        contributors_data = validated_data.pop("contributors", [])
        project = Project.objects.create(**validated_data)
        author_contributor, created = Contributor.objects.get_or_create(user=user)
        author_contributor.project.add(project)

        for username in contributors_data:
            try:
                contributor_user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(f"Utilisateur avec le nom d'utilisateur '{username}' n'existe pas.")
            contributor, created = Contributor.objects.get_or_create(user=contributor_user)
            contributor.project.add(project)

        return project

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.start_date = validated_data.get("start_date", instance.start_date)
        instance.type = validated_data.get("type", instance.type)

        contributors_data = validated_data.get("contributors", None)
        if contributors_data is not None:
            for username in contributors_data:
                try:
                    contributor_user = CustomUser.objects.get(username=username)
                except CustomUser.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Utilisateur avec le nom d'utilisateur '{username}' n'existe pas."
                    )
                contributor, created = Contributor.objects.get_or_create(user=contributor_user)
                contributor.project.add(instance)

        instance.save()
        return instance


class IssuesSerializerCreate(serializers.ModelSerializer):
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
        project_id = self.context["view"].kwargs.get("pk")
        project = get_object_or_404(Project, id=project_id)
        fields["assigned"].queryset = project.contributors.all()
        fields["project"].queryset = Project.objects.filter(id=project_id)
        return fields

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        return super().create(validated_data)


class IssuesSerializerUpdate(serializers.ModelSerializer):
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
        issue_id = self.context["view"].kwargs.get("pk")
        issue = get_object_or_404(Issues, id=issue_id)
        project = issue.project
        contributors = project.contributors.all()
        fields["assigned"].queryset = contributors
        fields["project"].queryset = Project.objects.filter(id=project.id)
        return fields

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class CommentsSerializerCreate(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    link = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ["id", "issue", "author", "description", "link", "uuid", "start_date"]
        read_only_fields = ["start_date", "uuid"]

    def get_link(self, obj):
        if obj.issue:
            return f"/api/issues/{obj.issue_id}/"
        return None

    def create(self, validated_data):
        user = self.context["request"].user
        contributor = Contributor.objects.get(user=user)
        validated_data["author"] = contributor
        return super().create(validated_data)

    def get_fields(self):
        fields = super().get_fields()
        issue_id = self.context["view"].kwargs.get("pk")
        fields["issue"].queryset = Issues.objects.filter(id=issue_id)
        return fields


class CommentsSerializerUpdate(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ["id", "issue", "author", "description", "link", "uuid", "start_date"]
        read_only_fields = ["start_date", "uuid", "issue", "link", "author"]

    def get_link(self, obj):
        return f"/api/issues/{obj.issue_id}/" if obj.issue else None

    def update(self, instance, validated_data):
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance
