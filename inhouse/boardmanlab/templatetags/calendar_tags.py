
from django import template
register = template.Library()

import calendar
from datetime import datetime

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

@register.simple_tag
def gen_day_string(value):
    return calendar.day_name[value]  #'Wednesday'

@register.simple_tag
def gen_month_string(value):
    return calendar.month_name[value].title()  #'March'

@register.simple_tag
def increment(value):
    if value == 12:
        return 1
    else:
        return value + 1  #'2'

@register.simple_tag
def decrement(value):
    if value == 1:
        return 12
    else:
        return value - 1  #'0'

@register.simple_tag
def increment_year(value, month):
    if month != 12:
        return value # same
    else:
        return value + 1

@register.simple_tag
def decrement_year(value, month):
    if month != 1:
        return value # same
    else:
        return value - 1






