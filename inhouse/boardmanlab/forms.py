from django import forms
from datetime import datetime
from users.models import User, Topic
from .models import helpSession
from reservations.models import Reservation

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

class FormCreateHelpSession(forms.ModelForm):
    class Meta:
        model = helpSession
        exclude = ['attendance', 'helper']
        fields = ['date', 'time', 'duration', 'topic', 'is_remote', 'is_inperson', 'remote_link', 'notes']

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(FormCreateHelpSession, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(FormCreateHelpSession, self).save(commit=False)
        inst.helper = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

    date = forms.DateField(
        label='date', 
        initial=today.date,
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'id' : 'form-picker-input'
                   }
            ),
        )
    time = forms.TimeField(
        label='time', 
        widget=forms.TimeInput(
            attrs={'type': 'time',
                   'id' : 'form-picker-input'
                   }
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
        choices=[(topic, topic) for topic in Topic.objects.all()],
        widget=forms.Select(
            attrs={'id': 'selectForm'}
            ),
        )

    is_inperson = forms.NullBooleanField(
        required = False,
        label = 'inperson',
        widget= forms.CheckboxInput(
            attrs={'id': 'checkboxForm'}
            ),
        )
    
    is_remote = forms.NullBooleanField(
        required = False,
        label = 'remote',
        widget= forms.CheckboxInput(
            attrs={'id': 'checkboxForm'}
            ),
        )

    remote_link = forms.CharField(
        required = False,
        label='remotelink',
        max_length=200,
        widget=forms.TextInput(
            attrs={'id': 'textAreaForm'}
            ),
        )

    notes = forms.CharField(
        required = False,
        label='notes',
        max_length=1000,
        widget=forms.Textarea(
            attrs={'id': 'textAreaForm'}
            ),
        )



class FormEditHelpSession(forms.ModelForm):
    class Meta:
        model = helpSession
        exclude = ['helper']
        fields = ['date', 'time', 'duration', 'topic', 'is_remote', 'is_inperson', 'remote_link', 'notes', 'attendance']

    date = forms.DateField(
        label='date', 
        widget=forms.DateInput(
            attrs={'type': 'date',
                   'id' : 'form-picker-input'}
            ),
        )
    time = forms.TimeField(
        label='time', 
        widget=forms.TimeInput(
            attrs={'type': 'time',
                   'id' : 'form-picker-input'}
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

    is_inperson = forms.NullBooleanField(
        required = False,
        label = 'inperson',
        widget= forms.CheckboxInput(
            attrs={'id': 'checkboxForm'}
            ),
        )
    
    is_remote = forms.NullBooleanField(
        required = False,
        label = 'remote',
        widget= forms.CheckboxInput(
            attrs={'id': 'checkboxForm'}
            ),
        )

    remote_link = forms.CharField(
        required = False,
        label='remotelink',
        max_length=200,
        widget=forms.TextInput(
            attrs={'id': 'textAreaForm'}
            ),
        )

    notes = forms.CharField(
        required = False,
        label='notes',
        max_length=1000,
        widget=forms.Textarea(
            attrs={'id': 'textAreaForm'}
            ),
        )

    attendance = forms.IntegerField(
        required = False,
        label='attendance',
        widget=forms.NumberInput(
            attrs={'id': 'textAreaForm'}
            ),
        )

class FormEditHelpSessionFeedback(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['helpSession', 'user']

    feedback = forms.CharField(
        label='Feedback',
        max_length=1000,
        widget=forms.Textarea(
            attrs={'id': 'textAreaForm'}
            ),
        )


class FormEditButton(forms.Form):
        helpSessionID = forms.IntegerField(
            widget=forms.NumberInput()
        )

class FormFeedbackButton(forms.Form):
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