from django.conf import settings
from datetime import datetime
year = datetime.now().year
month = datetime.now().month

class CalendarPathAdapter():

    def get_login_redirect_url():
        path = str(year) + "/" + str(month) + "/"
        return path