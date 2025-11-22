from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("signin/", views.signin),
    path("questions/", views.get_questions),
    path("submit/", views.submit_quiz),
]
