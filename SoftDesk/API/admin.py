from django.contrib import admin
from .models import Contributor, Project, Issues, Comments

admin.site.register(Contributor)
admin.site.register(Project)
admin.site.register(Issues)
admin.site.register(Comments)

# Register your models here.
