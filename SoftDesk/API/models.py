from django.db import models
from CustomUser.models import CustomUser


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(
        choices=[("Backend", "Backend"), ("Frontend", "Frontend"), ("IOS", "IOS"), ("Android", "Android")],
        max_length=100,
    )

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    project = models.ManyToManyField(Project, related_name="contributors")

    def __str__(self):
        projects = ", ".join([project.name for project in self.project.all()])
        return f"{self.user.username} - {projects}"
