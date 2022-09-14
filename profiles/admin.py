from django.contrib import admin
# import Profile model
from .models import Profile

# register the Profile model in admin (panel)
admin.site.register(Profile)