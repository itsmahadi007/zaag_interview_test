from django.apps import apps
from django.contrib import admin

for model in apps.get_app_config('cosmos').models.values():
    admin.site.register(model)