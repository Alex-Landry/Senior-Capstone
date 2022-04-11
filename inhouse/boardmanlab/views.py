from django.shortcuts import render
from oauth2_provider.views.generic import ProtectedResourceView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.shortcuts import redirect
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import *
from .models import helpSession
from reservations.models import Reservation
from users.models import User, Topic
from .forms import (
    FormEditHelpSessionFeedback,
    FormFeedbackButton,
    FormFilterDate,
    FormCreateHelpSession,
    FormDeleteHelpSession,
    FormEditHelpSession,
    FormEditButton,
    FormRecur,
    ProfileEdit,
)
import calendar

cal = calendar.Calendar()
cal.setfirstweekday(calendar.SUNDAY)


# Create your views here.


@login_required()
def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")

@login_required()
def profile(request):
    return render(request, "profile.html")

@login_required()
def profileEdit(request):
    editedUser = User.objects.get(pk=request.user.pk)
    if request.method=="POST":
        if "save" in request.POST:
            formEditUser = ProfileEdit(data=request.POST, instance=editedUser)
            if formEditUser.is_valid():
                editedUser = formEditUser.save()
                context = {"created_new": True}
                return render(request, "success.html", context)
            return render(request, 'profileEdit.html', {'ProfileEdit':formEditUser})

    context ={"ProfileEdit": ProfileEdit(instance=editedUser)}
    return render(request, 'profileEdit.html', context)


@login_required()
def calendarMonth(request, year, month, day):
    # session flag shows helpsessions on a given day (based on month)
    sessionflag = [0]

    if year == 0 and month == 0:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
    if day == 0 and month == datetime.now().month:
        day = datetime.now().day
    # session flag content
    for week in cal.monthdayscalendar(year, month):
        for dayz in week:
            if dayz != 0:
                # sessionflag list: index = date, value = number of help sessions
                sessionflag.append(
                    helpSession.objects.filter(
                        date__day=dayz, date__month=month
                    ).count()
                )
            else:
                continue
    context = {
        "day_string_list": [6, 0, 1, 2, 3, 4, 5],
        "day": day,
        "month": month,
        "year": year,
        "month_obj": cal.monthdayscalendar(year, month),
        "sessionflag": sessionflag,
    }
    return render(request, "calendarMonth.html", context)


@login_required()
def calendarDay(request, year, month, day):
    if request.method == "POST":

        key = request.POST["helpSessionID"]
        res_HelpSession = helpSession.objects.get(pk=key)

        # DELETE
        if "delete" in request.POST and res_HelpSession.helper.pk is request.user.pk:
            deleteform = FormDeleteHelpSession(request.POST)
            if deleteform.is_valid():
                key = deleteform.cleaned_data["helpSessionID"]
                res_HelpSession = helpSession.objects.get(pk=key)
                res_HelpSession.delete()

        # ATTEND
        if "attend" in request.POST:
            # Check to see if user is already signed up for helpSession
            if Reservation.objects.filter(
                user=request.user, helpSession=res_HelpSession
            ):
                already_attending = True
                new_reservation = False
            else:
                already_attending = False
                new_reservation = True
                ins = Reservation(user=request.user, helpSession=res_HelpSession)
                ins.save()
            # Set context for success page... if/else dependent
            context = {
                "already_attending": already_attending,
                "new_reservation": new_reservation,
            }
            return render(request, "success.html", context)

    if year == 0 and month == 0:
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
    if day == 0 and month == datetime.now().month:
        day = datetime.now().day
    helpSessions = helpSession.objects.filter(
        date__year=str(year), date__month=str(month), date__day=str(day)
    )
    context = {
        "helpSessions": helpSessions,
        "day_string_list": [6, 0, 1, 2, 3, 4, 5],
        "day": day,
        "month": month,
        "year": year,
        "FormEditButton": FormEditButton(),
        "FormDeleteHelpSession": FormDeleteHelpSession(),
        "month_obj": cal.monthdayscalendar(year, month),
    }
    return render(request, "calendarDay.html", context)


@login_required()
def helpsessions(request):
    user = request.user
    # this is for the filter (changes context)
    if request.method == "POST":
        # FILTER
        if "filter" in request.POST:
            filterform = FormFilterDate(request.POST)
            if filterform.is_valid():
                month = filterform.cleaned_data["month"]
                year = filterform.cleaned_data["year"]
                # list of reservations that match user, filtered by month/year
                reservations = Reservation.objects.filter(
                    user=user,
                    helpSession__date__year=year,
                    helpSession__date__month=month,
                ).order_by("-helpSession__date")
                # filter context
                context = {
                    "filterbool": True,
                    "reservations": reservations,
                    "already_attending": False,
                    "new_reservation": False,
                    "FormFilterDate": FormFilterDate(initial={"month": month}),
                    "FormFeedbackButton": FormFeedbackButton(),
                }
                # return filtered results
                return render(request, "helpSessions.html", context)
        # FEEDBACK
        if "feedback" in request.POST:
            # TODO
            feedbackform = FormFeedbackButton(request.POST)
            if feedbackform.is_valid():
                key = feedbackform.cleaned_data["helpSessionID"]
                reservation = Reservation.objects.filter(pk=key, user=request.user)
                context = {
                    "reservation": reservation,
                    "FormEditHelpSessionFeedback": FormEditHelpSessionFeedback(
                        instance=reservation
                    ),
                }
                return render(request, "helpSessionFeedback.html", context)

    # just render the page normally
    # list of reservations that match the user
    reservations = Reservation.objects.filter(user=user).order_by("-helpSession__date")
    context = {
        "filterbool": False,
        "reservations": reservations,
        "already_attending": False,
        "new_reservation": False,
        "FormFilterDate": FormFilterDate(),
        "FormFeedbackButton": FormFeedbackButton(),
    }

    return render(request, "helpSessions.html", context)


@login_required()
def managehelpsessions(request):
    # !!! wouldnt the admin like to see all help sessions and manage them? !!!
    helpsessions = helpSession.objects.filter(helper=request.user).order_by("-date")
    # Post requests
    if request.method == "POST":
        # FILTER
        if "filter" in request.POST:
            filterform = FormFilterDate(request.POST)
            if filterform.is_valid():
                month = filterform.cleaned_data["month"]
                year = filterform.cleaned_data["year"]
                helpsessions = helpSession.objects.filter(
                    helper=request.user, date__year=year, date__month=month
                ).order_by("-date")
                # filter context
                context = {
                    "helpSessions": helpsessions,
                    "created_new": False, # redundant?
                    "FormDeleteHelpSession": FormDeleteHelpSession(),
                    "FormEditButton": FormEditButton(),
                    "filterbool": True,
                    "FormFilterDate": FormFilterDate(initial={"month": month}),
                }
                # return filtered results
                return render(request, "manageHelpSessions.html", context)
        # DELETE
        if "delete" in request.POST:
            deleteform = FormDeleteHelpSession(request.POST)
            if deleteform.is_valid():
                key = deleteform.cleaned_data["helpSessionID"]
                res_HelpSession = helpSession.objects.get(pk=key)
                res_HelpSession.delete()
        # EDIT
        if "edit" in request.POST:
            editformbutton = FormEditButton(request.POST)
            if editformbutton.is_valid():
                pk = editformbutton.cleaned_data["helpSessionID"]
                instance = helpSession.objects.get(pk=pk)
                context = {
                    "helpSession": helpSession.objects.get(pk=pk),
                    "FormEditHelpSession": FormEditHelpSession(instance=instance),
                }
                return render(request, "editHelpSession.html", context)

        # if nothing is in the post request, but is still a post request?
        context = {
            "helpSessions": helpsessions,
            "created_new": False,
            "FormDeleteHelpSession": FormDeleteHelpSession(),
            "FormEditButton": FormEditButton(),
            "filterbool": False,
            "FormFilterDate": FormFilterDate(),
        }
        return render(request, "manageHelpSessions.html", context)

    # Base
    context = {
        "filterbool": False,
        "helpSessions": helpsessions,
        "created_new": False,
        "FormFilterDate": FormFilterDate(),
        "FormDeleteHelpSession": FormDeleteHelpSession(),
        "FormEditButton": FormEditButton(),
    }

    return render(request, "manageHelpSessions.html", context)


@login_required
def helpSessionFeedback(request):
    # TODO
    if request.method == "POST":
        if "save" in request.POST:
            # get the primary key of the reservation
            pk = request.POST.get("pk")
            # get the reservation
            # ambiguous variable name?
            helpSessionFeedbackEdit = Reservation.objects.get(pk=pk)
            editFeedbackForm = FormEditHelpSessionFeedback(
                data=request.POST, instance=helpSessionFeedbackEdit
            )
            if editFeedbackForm.is_valid():
                editFeedbackForm.save()
                context = {
                    "editedHelpSessionFeedback": True,
                }
            return render(request, "success.html", context)
    # Where does this 'helpSessionID' come from and what is it?
    key = request.POST.get("helpSessionID")
    helpSessionFeedbackEdit = Reservation.objects.get(pk=key, user=request.user)
    context = {
        "reservation": helpSessionFeedbackEdit,
        "FormEditHelpSessionFeedback": FormEditHelpSessionFeedback(
            instance=helpSessionFeedbackEdit
        ),
    }
    return render(request, "helpSessionFeedback.html", context)


@login_required
def editHelpSession(request):
    if request.method == "POST":
        if "save" in request.POST:
            pk = request.POST.get("pk")
            helpSessionEdit = helpSession.objects.get(pk=pk)
            editform = FormEditHelpSession(data=request.POST, instance=helpSessionEdit)
            if editform.is_valid():
                editform.save()
                # this might be old code from when this redirected to manage help sessions.
                helpsessions = helpSession.objects.filter(helper=request.user).order_by(
                    "-date"
                )
                context = {
                    "editedHelpSession": True,
                }
            return render(request, "success.html", context)
    # If request method isn't POST, load page
    # This IS a post request... we just never hit the above if's......
    helpSessionID = request.POST.get("helpSessionID")
    helpSessionEdit = helpSession.objects.get(pk=helpSessionID)
    context = {
        "helpSession": helpSessionEdit,
        "FormEditHelpSession": FormEditHelpSession(instance=helpSessionEdit),
    }
    return render(request, "editHelpSession.html", context)


@login_required()
def createHelpSession(request):
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    context = {
        "day": day,
        "month": month,
        "year": year,
        "FormCreateHelpSession": FormCreateHelpSession(user=request.user),
    }

    if request.method == "POST":
        # If user clicks 'create' save the helpsession and send them to success
        if "create" in request.POST:
            createform = FormCreateHelpSession(data=request.POST, user=request.user)
            if createform.is_valid():
                createform.save()
                context = {
                    "created_new": True,
                }
                return render(request, "success.html", context)
        # If user clicks 'recur' save the base helpsession and send them to recur page
        if "recur" in request.POST:
            createform = FormCreateHelpSession(data=request.POST, user=request.user)
            if createform.is_valid():
                base_hs = createform.save()
                context = {
                    "created_new": True,
                    "Form_Recur": FormRecur(),
                    "base_hs": base_hs,
                }
                return render(request, "recurHelpSession.html", context)

        if "setrecur" in request.POST:
            Form_Recur = FormRecur(request.POST)
            if Form_Recur.is_valid():
                # what type of recurrance (days, weeks, months)
                frequency = Form_Recur.cleaned_data["frequency"]
                # which days (if recur by week)
                recurdays = Form_Recur.cleaned_data["days"]
                # end date for recurrance
                end_date = Form_Recur.cleaned_data["end_date"]
                # get base help session (which recurrance is based on from POST)
                base_hs = helpSession.objects.get(pk=request.POST["helpSessionID"])
                # don't let more than a year get created at a time
                end_date_limiter = base_hs.date + relativedelta(years=1)
                if end_date_limiter < end_date:
                    end_date = end_date_limiter

                cur_hs_date = base_hs.date
                if frequency == "daily":
                    while cur_hs_date < end_date:
                        cur_hs_date += timedelta(days=1)
                        base_hs.date = cur_hs_date
                        base_hs.pk = None  # this ensures that a new helpsession object is created
                        base_hs.save()
                if frequency == "monthly":
                    while cur_hs_date < end_date:
                        cur_hs_date += relativedelta(months=1)
                        base_hs.date = cur_hs_date
                        base_hs.pk = None
                        base_hs.save()
                if frequency == "weekly":
                    while cur_hs_date < end_date:
                        cur_hs_date += relativedelta(days=1)
                        for day in recurdays:
                            if int(day) == cur_hs_date.weekday():
                                base_hs.date = cur_hs_date
                                base_hs.pk = None
                                base_hs.save()

                # Pass context to success page
                context = {
                    "recur_success": True,
                }
                return render(request, "success.html", context)

        # cancel recurrance
        if "cancel" in request.POST:
            temp_hs = helpSession.objects.get(pk=request.POST["helpSessionID"])
            temp_hs.delete()
            return redirect("/manageHelpSessions/")

    return render(request, "createHelpSession.html", context)


@login_required()
def recurHelpSession(request):
    return render(request, "recurHelpSession.html")


def success(request):
    return render(request, "success.html")


# AUTHORIZED ONLY VIEWS
class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            'Hello there! You are acting on behalf of "%s"\n' % (request.user)
        )


class Home(TemplateView):
    template_name = "home.html"


# Error Handling
def error_404(request, exception):
    data = {}
    return render(request, "errors/404.html", data)


def error_500(request):
    data = {}
    return render(request, "errors/500.html", data)


def error_400(request, exception):
    data = {}
    return render(request, "errors/400.html", data)


def error_403(request, exception):
    data = {}
    return render(request, "errors/403.html", data)
