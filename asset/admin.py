from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.HostList)
admin.site.register(models.Message)