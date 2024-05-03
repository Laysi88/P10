from django.db import models
from CustomUser.models import CustomUser
from uuid import uuid4


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
        project = ", ".join([project.name for project in self.project.all()])
        return f"{self.user.username}"


class Issues(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author")
    assigned = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name="assigned")
    priority = models.CharField(choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], max_length=100)
    nature = models.CharField(choices=[("Bug", "Bug"), ("Feature", "Feature"), ("Task", "Task")], max_length=100)
    status = models.CharField(
        choices=[("To Do", "To Do"), ("In Progress", "In Progress"), ("Finished", "Finished")],
        max_length=100,
        default="To Do",
    )

    def __str__(self):
        return self.title


class Comments(models.Model):
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    uuid = models.UUIDField(default=uuid4, editable=False)
