from django import forms
from datetime import datetime

date = datetime.now()

MONTHS = (
    ("1", "January"),
    ("2", "February"),
    ("3", "March"),
    ("4", "April"),
    ("5", "May"),
    ("6", "June"),
    ("7", "July"),
    ("8", "August"),
    ("9", "September"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December"),
)

YEARS = (
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
)

class CreateHelpSession(forms.Form):
    pass
    #date = forms.DateField(label='date', initial=datetime.date.today)
    #year = int(date.year)
    #month = int(date.month)
    #day = int(date.day)
    #time = forms.TimeField(label='time', initial=datetime.now())
    #hour = int(time.hour)
    #minute = int(time.minute)
    #duration = forms.IntegerField(label='duration', initial=30)
    #topic = forms.ModelChoiceField(queryset= User.objects.topics.all )
    #user = request.POST['user']

class FormFilterDate(forms.Form):
    month = forms.ChoiceField(
        choices=MONTHS,
        initial=MONTHS[date.month - 1],
        widget=forms.Select(
            attrs={'id': 'selectFilter'}
            ),
        )
    year = forms.ChoiceField(
        choices=YEARS,
        widget=forms.Select(
            attrs={'id': 'selectFilter'}
            ),
        )


class ProfileEdit(forms.Form):
    pass