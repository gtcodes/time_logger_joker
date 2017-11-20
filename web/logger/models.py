from django.db import models 
from django.utils.html import format_html
import django_tables2 as tables
import datetime

# Create your models here.

class User(models.Model):
    card_id = models.IntegerField(db_column='CARD_ID', primary_key=True) 
    first_name = models.CharField(db_column='FIRST_NAME', max_length=30) 
    last_name = models.CharField(db_column='LAST_NAME', max_length=30) 
    class_field = models.CharField(db_column='CLASS', max_length=15)  
    is_admin = models.IntegerField(db_column='IS_ADMIN')  

    def total_today(self):
        total = datetime.timedelta(0)
        for log in self.timelog_set.filter(start_time__gt=datetime.datetime.today().date()):
            total += log.delta()
        return total

    def __str__(self):
        return str(self.card_id) + " " + self.first_name

    class Meta:
        managed = False
        db_table = 'USER'

class Timelog(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  
    user = models.ForeignKey(User, db_column="card_id")  
    start_time = models.DateTimeField(db_column='START_TIME')  
    end_time = models.DateTimeField(db_column='END_TIME', blank=True, null=True)  
    # delta = end_time-start_time
    
    def delta(self):
        return self.end_time - self.start_time

    def __str__(self):
            return "id: " + str(self.id) + \
                    ", start_time: " + str(self.start_time) + \
                    ", end_time: " + str(self.end_time) + \
                    ", <User: " + str(self.user) + ">"
                    

    class Meta:
        managed = False
        db_table = 'TIMELOG'

class UserTable(tables.Table):

    def render_card_id(self, value):
        return format_html('<a href="{}">{}</a>', value, value)

    class Meta:
        model = User

