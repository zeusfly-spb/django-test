from django.urls import path
from polls.views import CurrentUserView, LogoutView
from . import views

app_name = "polls"  

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/results/", views.results, name="results"),
    path(
        "api/auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]

