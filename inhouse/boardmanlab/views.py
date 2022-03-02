from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from datetime import datetime
from .models import helpSession
from reservations.models import Reservation
from users.models import User, Topic
from .forms import FormFilterDate, FormCreateHelpSession, FormDeleteHelpSession, FormEditHelpSession, FormEditButton
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
    if request.method == "POST":
        
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
                new_reservation = False
            else:
                already_attending = False
                new_reservation = True
                ins = Reservation(user=user, helpSession=res_HelpSession)
                ins.save()
                    
            # get current reservations
            reservations = Reservation.objects.filter(user = user)

            context={
                "reservations": reservations,
                "already_attending": already_attending,
                "new_reservation": new_reservation,
                "FormFilterDate": FormFilterDate(),
                }

            return render(request, "helpSessions.html", context)

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
    # this is for the filter (changes context)
    if request.method == 'POST':
        filterform = FormFilterDate(request.POST)
        if filterform.is_valid():
            month = filterform.cleaned_data['month']
            year = filterform.cleaned_data['year']
            reservations = Reservation.objects.filter(user=user,
                                                    helpSession__date__year=year,
                                                   helpSession__date__month=month).order_by("-helpSession__date")
    # filter context
            context = {
                "filterbool": True,
                "reservations": reservations,
                "already_attending": False,
                "new_reservation": False,
                "FormFilterDate": FormFilterDate(initial={'month': month}),
                }
            # return filtered results
            return render(request, 'helpSessions.html', context)
    
    # just render the page normally
    reservations = Reservation.objects.filter(user = user).order_by("-helpSession__date")
    context = {
        "filterbool": False,
        "reservations": reservations,
        "already_attending": False,
        "new_reservation": False,
        "FormFilterDate": FormFilterDate(),
    }

    return render(request, 'helpSessions.html', context)

@login_required()
def managehelpsessions(request):
    helpsessions = helpSession.objects.filter(helper=request.user).order_by("-date")
    # Post requests
    if request.method == 'POST':
        #FILTER
        if 'filter' in request.POST:
            filterform = FormFilterDate(request.POST)
            if filterform.is_valid():
                month = filterform.cleaned_data['month']
                year = filterform.cleaned_data['year']
                helpsessions = helpSession.objects.filter(helper=request.user,
                                                        date__year=year,
                                                    date__month=month).order_by("-date")
                # filter context
                context = {
                    "helpSessions": helpsessions,
                    "created_new": False,
                    "FormDeleteHelpSession": FormDeleteHelpSession(),
                    "FormEditButton": FormEditButton(),
                    "filterbool": True,
                    "FormFilterDate": FormFilterDate(initial={'month': month}),
                    }
                # return filtered results
                return render(request, 'manageHelpSessions.html', context)
        #DELETE
        if "delete" in request.POST:
            deleteform = FormDeleteHelpSession(request.POST)
            if deleteform.is_valid():
                key = deleteform.cleaned_data['helpSessionID']
                res_HelpSession = helpSession.objects.get(pk=key)
                res_HelpSession.delete()
        #EDIT
        if "edit" in request.POST:
            editformbutton = FormEditButton(request.POST)
            if editformbutton.is_valid():
                pk = editformbutton.cleaned_data['helpSessionID']
                instance = helpSession.objects.get(pk=pk)
                context = {
                    "helpSession": helpSession.objects.get(pk=pk),
                    "FormEditButton": FormEditButton(),
                    "FormEditHelpSession": FormEditHelpSession(instance=instance),
                }
                return render(request, "editHelpSession.html", context)

            
        context = {
            "helpSessions": helpsessions,
            "created_new": False,
            "FormDeleteHelpSession": FormDeleteHelpSession(),
            "FormEditButton": FormEditButton(),
            "filterbool": False,
            "FormFilterDate": FormFilterDate(),
            }
        return render(request, 'manageHelpSessions.html', context)    

    # Base
    context = {
        "filterbool": False,
        "helpSessions": helpsessions,
        "created_new": False,
        "FormFilterDate": FormFilterDate(),
        "FormDeleteHelpSession": FormDeleteHelpSession(),
        "FormEditButton": FormEditButton(),
        }

    return render(request, 'manageHelpSessions.html', context)


@login_required
def editHelpSession(request):
    helpSessionTemp = request.POST["helpSession"]
    helpSessionEdit = helpSession.objects.get(pk=helpSessionTemp.pk)
    if request.method == 'POST':
        if 'save' in request.POST:
            editform = FormEditHelpSession(request.POST)
            if editform.is_valid():
                editform.save()
                helpsessions = helpSession.objects.filter(helper=request.user).order_by("-date")
                context={
                    "filterbool": False,
                    "helpSessions": helpsessions,
                    "created_new": True,
                    "FormFilterDate": FormFilterDate(),
                    "FormDeleteHelpSession": FormDeleteHelpSession(),
                    "FormEditButton": FormEditButton(),
                }
            return render(request, 'manageHelpSessions.html', context)
    context = {
        "helpSession": helpSessionEdit,
        "FormEditHelpSession": FormEditHelpSession(),
    }
    return render(request, 'editHelpSession.html', context)

@login_required()
def createHelpSession(request):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    context = {
        "day": day,
        "month": month,
        "year": year,
        "FormCreateHelpSession": FormCreateHelpSession()
    }

    if request.method=="POST":
        createform = FormCreateHelpSession(request.POST)
        if createform.is_valid():
            date = createform.cleaned_data['date']
            time = createform.cleaned_data['time']
            duration = createform.cleaned_data['duration']
            topic_pk = createform.cleaned_data['topic']
            topic = Topic.objects.get(pk=topic_pk)

            helpsessions = helpSession.objects.filter(helper=request.user).order_by("-date")

            context={
                "helpSessions": helpsessions,
                "created_new": True,
                "FormFilterDate": FormFilterDate(),
                "FormDeleteHelpSession": FormDeleteHelpSession(),
            }
            user = request.user
            ins = helpSession(helper=user, topic=topic, date=date, time=time, duration=duration)
            ins.save()
            return render(request, "manageHelpSessions.html", context)
    if request.method=="POST":
        deleteform = FormDeleteHelpSession(request.POST)
        if deleteform.is_valid():
            key = deleteform.cleaned_data['helpSessionID']
            res_HelpSession = helpSession.objects.get(pk=key)
            res_HelpSession.delete()

            helpsessions = helpSession.objects.filter(helper=request.user).order_by("-date")
            context = {
                "helpSessions": helpsessions,
                "created_new": False,
                "FormFilterDate": FormFilterDate(),
                "FormDeleteHelpSession": FormDeleteHelpSession(),
                }
        return render(request, 'manageHelpSessions.html', context)

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