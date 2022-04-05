from django import forms
from datetime import datetime
from users.models import User, Topic
from .models import User, ClassStanding


class FormMyAccountEdit(forms.ModelForm):
    class Meta:
        model=User
        exclude= ["is_student", "is_helper", "is_admin", "picture", "first_name", "last_name", "topics", "position", "classStanding"]
    

    classStanding = forms.ChoiceField(
        choices=[(standing, standing) for standing in ClassStanding.objects.all()],
        widget=forms.Select(
        attrs={'id': 'selectForm'}
                                )
                                   )
 
    topics = forms.MultipleChoiceField(
        choices=[(topic, topic) for topic in Topic.objects.all()],
        widget=forms.Textarea(attrs={'id': 'selectForm'})
                                    )
    
    position = forms.CharField(
        required = False,
        label = "position",
        max_length=10,
        widget=forms.Textarea(attrs={"id": "textAreaForm"}),
    )

    personalBio = forms.CharField(
        label ="Bio",
        max_length=1000,
        widget=forms.Textarea(attrs={"id": "textAreaForm"}),
    )