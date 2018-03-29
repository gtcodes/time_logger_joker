from django.utils.html import format_html
from logger.models import User
from functools import reduce
import django_tables2 as tables
import math
import datetime

class UserTable(tables.Table):

    def render_card_id(self, value):
        return format_html('<a href="{}">{}</a>', value, value)

    class Meta:
        model = User

class DayTable(tables.Table):
    user = tables.Column(order_by=('user.last_name', 'user.first_name'))
    attendance = tables.Column()
    starttimes = tables.Column()
    endtimes = tables.Column()
    
    def render_user(self, value):
        return format_html('<a href="{}">{}</a>', 
                    "/logger/user/"+str(value.card_id),
                    value.last_name.capitalize() +" "+ value.first_name.capitalize())

    def render_attendance(self, value):
        if(isinstance(value, datetime.timedelta)):
            return math.floor(value.seconds/60)
        else: 
            return value

    def render_starttimes(self, value):
        return reduce((lambda x,y: (x.strftime("%H:%M:%S") if not isinstance(x, str) else x) + ",  " + (y.strftime("%H:%M:%S") if not isinstance(y, str) else y)), value)
    
    def render_endtimes(self, value):
        return reduce((lambda x,y: (x.strftime("%H:%M:%S") if not isinstance(x, str) else x) + ",  " + (y.strftime("%H:%M:%S") if not isinstance(y, str) else y)), value)
