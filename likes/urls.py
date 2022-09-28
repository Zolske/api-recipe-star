# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.urls import path
from likes import views

urlpatterns = [
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
]