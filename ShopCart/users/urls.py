from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import signup, session_activity


urlpatterns = [
    path("signup/", signup, name="signup"),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "session-activity/",
        session_activity,
        name="session_activity",
    ),
]