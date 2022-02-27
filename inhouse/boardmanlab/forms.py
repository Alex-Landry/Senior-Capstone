from django import forms
import datetime

class CreateHelpSession(forms.Form):

    date = forms.DateField(label='date', initial=datetime.date.today)
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    time = forms.TimeField(label='time', initial=datetime.now())
    hour = int(time.hour)
    minute = int(time.minute)
    duration = forms.IntegerField(label='duration', initial=30)
    topic = forms.ModelChoiceField(queryset= User.objects.topics.all )
    user = request.POST['user']


    your_name = forms.CharField(label='Your name', max_length=100)


class ProfileEdit(forms.Form):
    pass