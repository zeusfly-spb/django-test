from django.urls import path
from polls.views import CurrentUserView, LogoutView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "api/auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]