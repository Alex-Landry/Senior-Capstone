from django.shortcuts import render
from django.http import HttpResponse
from reservations.models import Reservation

# Create your views here.
def new_help_session(request):
    if request.method=="POST":
        helpSession = request.POST['helpSession']
        user = request.POST['user']
        helper = helpSession.helper
        topic = helpSession.topic
        time = helpSession.time

        context={
            "helper": helper,
            "topic": topic,
            "time": time
        }
        ins = Reservation(user=user, helpSession=helpSession)
        ins.save()
        return render(request, "successful_booking.html", context)

    return render(request, 'new_help_session_student_view.html')