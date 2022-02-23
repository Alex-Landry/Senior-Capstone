from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from datetime import datetime
from .models import helpSession
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
def calendarMonth(request, year, month, day):
    if year == 0 and month == 0:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
    if day == 0 and month == datetime.now().month:
        day = datetime.now().day
    context = {
        "day_string_list": [6,0,1,2,3,4,5],
        "day": day,
        "month": month,
        "year": year,
        "month_obj": cal.monthdayscalendar(year, month),
    }
    return render(request, 'calendarMonth.html', context)

@login_required()
def calendarDay(request, year, month, day):
    if year == 0 and month == 0:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
    if day == 0 and month == datetime.now().month:
        day = datetime.now().day
    context = {
        "day_string_list": [6,0,1,2,3,4,5],
        "day": day,
        "month": month,
        "year": year,
        "month_obj": cal.monthdayscalendar(year, month),
    }
    return render(request, 'calendarDay.html', context)

@login_required()
def helpsessions(request):
    return render(request, 'helpSessions.html')

@login_required()
def createHelpSession(request):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    context = {
        "day": day,
        "month": month,
        "year": year,
    }

    if request.method=="POST":
        date = request.POST['date']
        time = request.POST['time']
        duration = request.POST['duration']
        topic = request.POST['topic']
        user = user

        context={
            "date": date,
            "time": topic,
            "duration": time,
            "topic": topic,
            "user": user,
        }

        date = datetime.combine(datetime.date(date), datetime.time(time))

        ins = helpSession(helper=user, topic=topic, date=date, duration=duration)
        ins.save()
        return render(request, "/helpsessions.html", context)

    return render(request, 'createHelpSession.html')

    ##

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



# Error Handling
def error_404(request, exception):
        data = {}
        return render(request,'errors/404.html', data)

def error_500(request):
        data = {}
        return render(request,'errors/500.html', data)

def error_400(request, exception):
        data = {}
        return render(request,'errors/400.html', data)

def error_403(request,  exception):
        data = {}
        return render(request,'errors/403.html', data)