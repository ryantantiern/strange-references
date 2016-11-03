from django.contrib import admin

from .models import Reference

# include the References model in the admin panel
admin.site.register(Reference)
