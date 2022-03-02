from django import forms
from datetime import datetime
from users.models import User, Topic
from .models import helpSession

today = datetime.now()

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

class FormCreateHelpSession(forms.Form):

    date = forms.DateField(
        label='date', 
        initial=today.date,
        widget=forms.DateInput(
            attrs={'type': 'date'}
            ),
        )
    time = forms.TimeField(
        label='time', 
        widget=forms.TimeInput(
            attrs={'type': 'time'}
            ),
        )
    duration = forms.ChoiceField(
        choices=[(i, i) for i in range(15, 130, 15)],
        label='duration', 
        initial=30,
        widget=forms.Select(
            attrs={'id': 'selectForm'}
            ),
        )
    topic = forms.ChoiceField(
        choices=[(topic.pk, topic) for topic in Topic.objects.all()],
        widget=forms.Select(
            attrs={'id': 'selectForm'}
            ),
        )


class FormEditHelpSession(forms.ModelForm):
    class Meta:
        model = helpSession
        exclude = ['helper', 'attendance']

    date = forms.DateField(
        label='date', 
        widget=forms.DateInput(
            attrs={'type': 'date'}
            ),
        )
    time = forms.TimeField(
        label='time', 
        widget=forms.TimeInput(
            attrs={'type': 'time'}
            ),
        )
    duration = forms.ChoiceField(
        choices=[(i, i) for i in range(15, 130, 15)],
        label='duration',
        widget=forms.Select(
            attrs={'id': 'selectForm'}
            ),
        )
    topic = forms.ChoiceField(
        choices=[(topic.topic, topic.topic) for topic in Topic.objects.all()],
        widget=forms.Select(
            attrs={'id': 'selectForm'}
            ),
        )

class FormEditButton(forms.Form):
        helpSessionID = forms.IntegerField(
            widget=forms.NumberInput()
        )
        
    
# Form for filtering by month, year
class FormFilterDate(forms.Form):
    month = forms.ChoiceField(
        choices=MONTHS,
        initial=MONTHS[today.month - 1],
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

class FormDeleteHelpSession(forms.Form):
    helpSessionID = forms.IntegerField(
        widget=forms.NumberInput()
    )
    pass



class ProfileEdit(forms.Form):
    pass