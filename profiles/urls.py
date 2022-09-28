# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.urls import path
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]