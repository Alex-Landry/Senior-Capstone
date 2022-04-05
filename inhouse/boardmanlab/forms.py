from django import forms
from datetime import datetime
from users.models import User, Topic, ClassStanding, Position
from .models import helpSession
from reservations.models import Reservation

today = datetime.now()
DAYS = (
    ("6", "Sunday"),
    ("0", "Monday"),
    ("1", "Tuesday"),
    ("2", "Wednesday"),
    ("3", "Thursday"),
    ("4", "Friday"),
    ("5", "Saturday"),
)

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
        exclude = ["attendance", "helper"]
        fields = [
            "date",
            "time",
            "duration",
            "topic",
            "is_remote",
            "is_inperson",
            "remote_link",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user")
        super(FormCreateHelpSession, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(FormCreateHelpSession, self).save(commit=False)
        inst.helper = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst

    date = forms.DateField(
        label="date",
        initial=today.date,
        widget=forms.DateInput(attrs={"type": "date", "id": "form-picker-input"}),
    )
    time = forms.TimeField(
        label="time",
        widget=forms.TimeInput(attrs={"type": "time", "id": "form-picker-input"}),
    )
    duration = forms.ChoiceField(
        choices=[(i, i) for i in range(15, 130, 15)],
        label="duration",
        initial=30,
        widget=forms.Select(attrs={"id": "select-form"}),
    )

    # try getting choices (if in db)
    try:
        choicesGen=[(topic, topic) for topic in Topic.objects.all()]
    # except just give it something
    except:
        choicesGen=[('topic', 'topic')]

    topic = forms.ChoiceField(
        choices=choicesGen,
        widget=forms.Select(attrs={"id": "select-form"}),
    )

    is_inperson = forms.NullBooleanField(
        required=False,
        label="inperson",
        widget=forms.CheckboxInput(attrs={"id": "checkbox-form"}),
    )

    is_remote = forms.NullBooleanField(
        required=False,
        label="remote",
        widget=forms.CheckboxInput(attrs={"id": "checkbox-form"}),
    )

    remote_link = forms.CharField(
        required=False,
        label="remotelink",
        max_length=200,
        widget=forms.TextInput(attrs={"id": "text-area-form"}),
    )

    notes = forms.CharField(
        required=False,
        label="notes",
        max_length=1000,
        widget=forms.Textarea(attrs={"id": "text-area-form"}),
    )


class FormEditHelpSession(forms.ModelForm):
    class Meta:
        model = helpSession
        exclude = ["helper"]
        fields = [
            "date",
            "time",
            "duration",
            "topic",
            "is_remote",
            "is_inperson",
            "remote_link",
            "notes",
            "attendance",
        ]

    date = forms.DateField(
        label="date",
        widget=forms.DateInput(attrs={"type": "date", "id": "form-picker-input"}),
    )
    time = forms.TimeField(
        label="time",
        widget=forms.TimeInput(attrs={"type": "time", "id": "form-picker-input"}),
    )
    duration = forms.ChoiceField(
        choices=[(i, i) for i in range(15, 130, 15)],
        label="duration",
        widget=forms.Select(attrs={"id": "select-form"}),
    )

    # try getting choices (if in db)
    try:
        choicesGen=[(topic, topic) for topic in Topic.objects.all()]
    except:
        choicesGen=[('topic', 'topic')]

    topic = forms.ChoiceField(
        choices=choicesGen,
        widget=forms.Select(attrs={"id": "select-form"}),
    )

    is_inperson = forms.NullBooleanField(
        required=False,
        label="inperson",
        widget=forms.CheckboxInput(attrs={"id": "checkbox-form"}),
    )

    is_remote = forms.NullBooleanField(
        required=False,
        label="remote",
        widget=forms.CheckboxInput(attrs={"id": "checkbox-form"}),
    )

    remote_link = forms.URLField(
        required=False,
        label="remotelink",
        max_length=200,
        widget=forms.URLInput(attrs={"id": "text-area-form"}),
    )

    notes = forms.CharField(
        required=False,
        label="notes",
        max_length=1000,
        widget=forms.Textarea(attrs={"id": "text-area-form"}),
    )

    attendance = forms.IntegerField(
        required=False,
        label="attendance",
        widget=forms.NumberInput(attrs={"id": "text-area-form"}),
    )


class FormEditHelpSessionFeedback(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ["helpSession", "user"]

    feedback = forms.CharField(
        label="Feedback",
        max_length=1000,
        widget=forms.Textarea(attrs={"id": "text-area-form"}),
    )


class FormEditButton(forms.Form):
    helpSessionID = forms.IntegerField(widget=forms.NumberInput())


class FormFeedbackButton(forms.Form):
    helpSessionID = forms.IntegerField(widget=forms.NumberInput())


# Form for filtering by month, year
class FormFilterDate(forms.Form):
    month = forms.ChoiceField(
        choices=MONTHS,
        initial=MONTHS[today.month - 1],
        widget=forms.Select(attrs={"id": "select-filter"}),
    )
    year = forms.ChoiceField(
        choices=YEARS,
        widget=forms.Select(attrs={"id": "select-filter"}),
    )


class FormDeleteHelpSession(forms.Form):
    helpSessionID = forms.IntegerField(widget=forms.NumberInput())


class FormRecur(forms.Form):

    helpSessionID = forms.IntegerField(
        widget=forms.NumberInput(attrs={"type": "hidden"})
    )

    frequency = forms.ChoiceField(
        required=True,
        label="kindof",
        choices=[("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")],
        widget=forms.Select(
            attrs={
                "id": "select-form",
            }
        ),
    )

    days = forms.MultipleChoiceField(
        required=False,
        label="days",
        choices=DAYS,
        widget=forms.CheckboxSelectMultiple(attrs={"id": "checkbox-form"}),
    )

    end_date = forms.DateField(
        required=True,
        label="date",
        widget=forms.DateInput(attrs={"type": "date", "id": "form-picker-input"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get("frequency")
        days = cleaned_data.get("days")

        if frequency == "days" and not days:
            raise ValidationError(
                "Need to specify which days to recur on if frequency is days."
            )


class ProfileEdit(forms.ModelForm):
    class Meta:
        model=User
        exclude= ["is_student", "is_helper", 
        "is_admin", "password", "username", 
        "date_joined", "first_name", "last_name", 
        "email", "picture", "is_active", "is_staff",
        "is_superuser", "last_login", "user_permissions",
        "groups"]
    

    classStanding = forms.ModelChoiceField(
                required=False,
                queryset=ClassStanding.objects.all(),
                widget=forms.Select(attrs={"id": "select-form"}),
                )

    position = forms.ModelChoiceField(
                required=False,
                queryset=Position.objects.all(),
                widget=forms.Select(attrs={"id": "select-form"}),
                )
                            
 
    topics = forms.ModelMultipleChoiceField(
                required=False,
                queryset=Topic.objects.all(),
                widget=forms.CheckboxSelectMultiple(attrs={"id": "select-form"}),
                )
    

    personalBio = forms.CharField(
                required=False,
                max_length=1000,
                widget=forms.Textarea(attrs={"id": "text-area-form"}),
                )
