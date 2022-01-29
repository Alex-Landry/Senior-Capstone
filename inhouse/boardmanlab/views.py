from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def calendar(request):
    return render(request, 'calendar.html')

def helpsessions(request):
    return render(request, 'my_help_sessions_student_view.html')

def error(request):
    return render(request, 'error.html')