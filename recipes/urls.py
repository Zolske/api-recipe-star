# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.urls import path
from recipes import views

urlpatterns = [
    path('recipes/', views.RecipeList.as_view()),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view())
]