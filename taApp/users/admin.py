from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.StudentProfile)
admin.site.register(models.ProfessorProfile)
admin.site.register(models.Requests)
