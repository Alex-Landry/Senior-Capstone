from django.shortcuts import render
from django.http import HttpResponse
from reservations.models import Reservation

# Create your views here.
def new_help_session(request):
    if request.method=="POST":
        helper = request.POST['helper']
        topic = request.POST['topic']
        time = request.POST['time']

        context={
            "helper": helper,
            "topic": topic,
            "time": time
        }
        ins = Reservation(topic=topic, duration=time, student='Ben', helper=helper)
        ins.save()
        return render(request, "successful_booking.html", context)

    return render(request, 'new_help_session_student_view.html')