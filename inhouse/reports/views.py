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
    response['Content-Disposition'] = 'attachment; filename=course_freq.csv'

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

@login_required()
def helper_freq_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=helper_freq.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    helper_freq = Reservation.objects.values('helpSession__helper__username', 'helpSession__helper__first_name', 'helpSession__helper__last_name').annotate(total=Count('id'))

    # Add column headings to the csv file
    writer.writerow(['Helper', 'First Name', 'Last Name', 'Signed Up'])

    # Loop Through and output
    for item in helper_freq:
        writer.writerow([item['helpSession__helper__username'], item['helpSession__helper__first_name'], 
        item['helpSession__helper__last_name'], item['total']])
    
    return response
