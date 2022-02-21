from django.shortcuts import render

# Create your views here.


def update_user_social_data(strategy, *args, **kwargs):
  response = kwargs['response']
  backend = kwargs['backend']
  user = kwargs['user']

  if response['picture']:
    url = response['picture']
    userProfile_obj = User()
    userProfile_obj.user = user
    userProfile_obj.picture = url
    userProfile_obj.save()