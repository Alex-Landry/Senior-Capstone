from django.urls import path, include

from . import views

urlpatterns = [
    path("/home/", views.index, name="index"),
    path("", views.login, name="login"),
    path('/profile', views.profile, name='profile'),
    path('/profileEdit', views.profileEdit, name='profileEdit'),
    path('/analytics', views.analytics, name="analytics"),
    path("/helpsessions/", views.helpsessions, name="helpsessions"),
    path("/manageHelpSessions/", views.managehelpsessions, name="manageHelpSessions"),
    path("/createHelpSession/", views.createHelpSession, name="createHelpSession"),
    path("/recurHelpSession/", views.recurHelpSession, name="recurHelpSession"),
    path("/editHelpSession/", views.editHelpSession, name="editHelpSession"),
    path("/helpSessionFeedback/", views.helpSessionFeedback, name="helpSessionFeedback"),
    path("calendar", views.calendar, name="calendar"),
    path(
        "calendarMonth/<int:year>/<int:month>/<int:day>/",
        views.calendarMonth,
        name="calendarMonth",
    ),
    path(
        "calendarDay/<int:year>/<int:month>/<int:day>/",
        views.calendarDay,
        name="calendarDay",
    ),
    path("/success/", views.success, name="success"),
    path("/accounts/", include("allauth.urls")),
]
