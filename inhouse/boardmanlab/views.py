from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
import calendar
cal = calendar.Calendar()
cal.setfirstweekday(calendar.SUNDAY)


# Create your views here.

@login_required()
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

@login_required()
def calendar(request):
    context = {
        "day_string_list": [6,0,1,2,3,4,5],
        "day": datetime.now().day,
        "month": datetime.now().month,
        "year": datetime.now().year,
        "month_obj": cal.monthdayscalendar(datetime.now().year, datetime.now().month),
    }
    return render(request, 'calendar.html', context)

@login_required()
def helpsessions(request):
    return render(request, 'my_help_sessions_student_view.html')

def error(request):
    return render(request, 'error.html')


#AUTHORIZED ONLY VIEWS
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            'Hello there! You are acting on behalf of "%s"\n'
            % (request.user))


class Home(TemplateView):
    template_name = 'home.html'