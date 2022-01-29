from django.urls import path

from . import views

urlpatterns = [
    path('/home', views.index, name='index'),
    path('', views.login, name='login'),
    path('/helpsessions', views.helpsessions, name='helpsessions'),
    path('/calendar', views.helpsessions, name='calendar'),
    path('/error', views.error, name='error'),
]