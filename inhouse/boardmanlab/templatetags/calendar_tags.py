from django import template

register = template.Library()
from reservations.models import Reservation
from users.models import User

import calendar
from datetime import datetime
from datetime import timedelta

# Get the current month: return obj
@register.simple_tag
def get_month():
    return datetime.now().month


# Get the current year: return obj
# DANGER
@register.simple_tag
def get_month():
    return datetime.now().year


# Generate month object for calendar genertation: return obj
@register.simple_tag
def month_obj(year, month):
    return datetime.monthdayscalendar(year, month)


# This is used for the labels for the top of the month view
@register.simple_tag
def gen_day_string(value):
    return calendar.day_name[value]  #'Wednesday'


# This is used for the day view (generated day string)
# parameters = int, int, int
@register.simple_tag
def get_day_string(year, month, day):
    day = datetime(year, month, day).weekday()
    return calendar.day_name[day]


@register.simple_tag
def gen_month_string(value):
    return calendar.month_name[value].title()  #'March'

# returns next date (tomorrow)
@register.simple_tag
def increment_day(year, month, day):
    day = datetime(year, month, day)
    day = day + timedelta(days=1)
    return day.day

# returns previous date (yesterday)
@register.simple_tag
def decrement_day(year, month, day):
    date = datetime(year, month, day)
    date = date - timedelta(days=1)
    return date.day

# gets the next month (int) for calendarday
@register.simple_tag
def increment_month(year, month, day):
    date = datetime(year, month, day)
    date = date + timedelta(days=1)
    return date.month

# gets the previous month (int) for calendarday
@register.simple_tag
def decrement_month(year, month, day):
    date = datetime(year, month, day)
    date = date - timedelta(days=1)
    return date.month

# gets the next month (int) for calendarmonth
@register.simple_tag
def increment_month_alt(year, month, day):
    if month == 12:
        return 1
    else:
        return month + 1

# gets the previous month (int) for calendarmonth
@register.simple_tag
def decrement_month_alt(year, month, day):
    if month == 1:
        return 12
    else:
        return month - 1

# gets the next year
@register.simple_tag
def increment_year(year, month):
    if month != 12:
        return year  # same
    else:
        return year + 1

# gets the previous year
@register.simple_tag
def decrement_year(year, month):
    if month != 1:
        return year  # same
    else:
        return year - 1

# returns a string of the time + duration
@register.simple_tag
def add_minutes(date, time, duration):
    endtime = datetime.combine(date, time) + timedelta(minutes=duration)
    endtime = endtime.time().strftime("%I:%M %p")
    if endtime[0] == "0":
        endtime = endtime[1:]
    return endtime

# formats time into a string object
@register.simple_tag
def time_format(time):
    time = time.strftime("%I:%M %p")
    if time[0] == "0":
        time = time[1:]
    return time

# UNSURE of what this does
@register.simple_tag
def set_pk(aform, helpSessionpk):
    aform = helpSessionpk
    return aform

# generates a day string('wednesday') from datetime object
@register.simple_tag
def get_day_string_from_datetime(datetimeobj):
    return datetimeobj.strftime("%A")

# indexes a list from a indexable list and an index
@register.filter
def index(indexable, i):
    return indexable[i]

# return the number of students signed up for a particular help session
@register.simple_tag
def get_student_sign_up(cur_helpsession):
    return Reservation.objects.filter(helpSession=cur_helpsession).count()

# checks if some parameter is the string 'days'
# this could be unused code
@register.simple_tag
def get_freq(freq):
    if freq == "days":
        return True

@register.simple_tag
def get_number_of_users():
    return User.objects.all().count()

@register.simple_tag
def get_current_number_of_users():
    today = datetime.date.today()
    last_week = today - datetime.timedelta(days=7)
    return User.objects.filter(last_login__range=(last_week, today)).count()



