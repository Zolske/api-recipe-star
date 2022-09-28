# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.contrib import admin
# import Profile model
from .models import Profile

# register the Profile model in admin (panel)
admin.site.register(Profile)