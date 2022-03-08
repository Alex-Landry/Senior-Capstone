from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from boardmanlab.models import helpSession
from reservations.models import Reservation
import csv

@login_required()
def helpsessions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=helpsessions.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    reservations = Reservation.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Helper', 'Topic', 'Date', 'Time', 'Duration', 'Attendance', 'Feedback'])

    # Loop Through and output
    for reservation in reservations:
        writer.writerow([reservation.helpSession.helper, reservation.helpSession.topic, reservation.helpSession.date, 
        reservation.helpSession.time, reservation.helpSession.duration, reservation.helpSession.attendance, reservation.feedback])
    
    return response
