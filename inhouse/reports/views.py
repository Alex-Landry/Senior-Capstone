from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from boardmanlab.models import helpSession
from reservations.models import Reservation
import csv

@login_required()
def course_freq_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=helpsessions.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    course_freq = Reservation.objects.values('helpSession__topic').annotate(total=Count('id'))

    # Add column headings to the csv file
    writer.writerow(['Topic', 'Signed Up'])

    # Loop Through and output
    for item in course_freq:
        writer.writerow([item['helpSession__topic'], item['total']])
    
    return response
