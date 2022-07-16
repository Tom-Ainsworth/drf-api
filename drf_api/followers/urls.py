from django.urls import path
from drf_api.followers import views

urlpatterns = [
    path("followers/", views.FollowerList.as_view()),
    path("followers/<int:pk>", views.FollowerDetail.as_view()),
]
