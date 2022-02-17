
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










