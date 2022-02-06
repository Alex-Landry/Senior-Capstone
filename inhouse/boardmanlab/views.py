from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
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

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')