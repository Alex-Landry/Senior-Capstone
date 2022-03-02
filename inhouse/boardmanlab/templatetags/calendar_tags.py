
from django import template
register = template.Library()

import calendar
from datetime import datetime
from datetime import timedelta

# Get the current month: return obj
@register.simple_tag
def get_month():
    return datetime.now().month

# Get the current year: return obj
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

@register.simple_tag
def increment_day(year, month, day):
    day = datetime(year, month, day)
    day = day + timedelta(days = 1)
    return day.day

@register.simple_tag
def decrement_day(year, month, day):
    date = datetime(year, month, day)
    date = date - timedelta(days = 1)
    return date.day

@register.simple_tag
def increment_month(year, month, day):
    date = datetime(year, month, day)
    date = date + timedelta(days = 1)
    return date.month

@register.simple_tag
def decrement_month(year, month, day):
    date = datetime(year, month, day)
    date = date - timedelta(days = 1)
    return date.month

@register.simple_tag
def increment_month_alt(year, month, day):
    if month == 12:
        return 1
    else:
        return month + 1

@register.simple_tag
def decrement_month_alt(year, month, day):
    if month == 1:
        return 12
    else:
        return month - 1

@register.simple_tag
def increment_year(year, month):
    if month != 12:
        return year # same
    else:
        return year + 1

@register.simple_tag
def decrement_year(year, month):
    if month != 1:
        return year # same
    else:
        return year - 1

@register.simple_tag
def add_minutes(date, time, duration):
    endtime = datetime.combine(date, time) + timedelta(minutes = duration)
    endtime = endtime.time().strftime("%I:%M %p")
    if endtime[0] == '0':
        endtime = endtime[1:]
    return endtime

@register.simple_tag
def time_format(time):
    time = time.strftime("%I:%M %p").replace(' 0', '')
    return time

@register.simple_tag
def set_pk(aform, helpSessionpk):
    aform = helpSessionpk
    return aform

@register.simple_tag
def get_day_string_from_datetime(datetimeobj):
    return datetimeobj.strftime('%A')

