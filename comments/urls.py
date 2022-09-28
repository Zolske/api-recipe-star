# The code is based on  "Adam Lapinski's" walk-through project "Moments"!
# https://github.com/Code-Institute-Solutions/moments

from django.urls import path
from comments import views

urlpatterns = [
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view())
]