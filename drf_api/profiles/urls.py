from django.urls import path
from drf_api.profiles import views

urlpatterns = [
    path("profiles/", views.ProfileList.as_view()),
]
