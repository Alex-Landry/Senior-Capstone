from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from datetime import datetime
from .models import helpSession
from reservations.models import Reservation
from users.models import User
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
    if request.method=="POST":
        
        key = request.POST['helpSession']
        res_HelpSession = helpSession.objects.get(pk=key)
        key = request.POST['user']
        user = User.objects.get(pk=key)

        #check request for delete
        try:
            delete = request.POST['delete']
            if delete:
                res_HelpSession.delete()
        except:
            # Check to see if user is already signed up for helpSession
            if Reservation.objects.filter(user=user, helpSession=res_HelpSession):
                already_attending = True
            else:
                already_attending = False
                ins = Reservation(user=user, helpSession=res_HelpSession)
                ins.save()
                    
            # get current reservations
            reservations = Reservation.objects.filter(user = user)

            context={
                "reservations": reservations,
                "already_attending": already_attending,
                }

            return render(request, "helpSession_booked.html", context)

    if year == 0 and month == 0:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
    if day == 0 and month == datetime.now().month:
        day = datetime.now().day
    helpSessions = helpSession.objects.filter(date__year=str(year), date__month=str(month), date__day=str(day))
    context = {
        "helpSessions": helpSessions,
        "day_string_list": [6,0,1,2,3,4,5],
        "day": day,
        "month": month,
        "year": year,
        "month_obj": cal.monthdayscalendar(year, month),
    }
    return render(request, 'calendarDay.html', context)


        
@login_required()
def helpsessions(request):
    user = request.user
    reservations = Reservation.objects.filter(user = user)
    context = {
        "reservations": reservations,
    }

    return render(request, 'helpSessions.html', context)

@login_required()
def managehelpsessions(request):
    helpsessions = helpSession.objects.filter(helper=request.user).order_by("-date")
    user = request.user
    reservations = Reservation.objects.filter(user = user)
    context = {
        "helpSessions": helpsessions,
        "reservations": reservations,
    }

    return render(request, 'manageHelpSessions.html', context)

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
        dateString = request.POST['date']
        year = int(dateString.split('-')[0])
        month = int(dateString.split('-')[1])
        day = int(dateString.split('-')[2])
        time = request.POST['time']
        timeString = time
        hour = int(timeString.split(':')[0])
        minute = int(timeString.split(':')[1])
        date = datetime(year, month, day, hour, minute)
        duration = request.POST['duration']
        topic = request.POST['topic']
        user = request.POST['user']
        reservations = Reservation.objects.filter(user=request.user)

        context={
            "date": date,
            "time": time,
            "duration": duration,
            "topic": topic,
            "user": request.user,
            "reservations": reservations,
            "created_new": True,
        }
        user = request.user
        ins = helpSession(helper=user, topic=topic, date=date, time=date.time(), duration=duration)
        ins.save()
        return render(request, "manageHelpSessions.html", context)

    return render(request, 'createHelpSession.html', context)


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