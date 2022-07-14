from django.urls import path
from drf_api.posts import views

urlpatterns = [
    path("posts/", views.PostList.as_view()),
]
