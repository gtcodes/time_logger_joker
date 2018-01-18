from django.db import models 
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
        return self.first_name.lower() + " " + self.last_name.lower()

    def __lt__(self, other):
        return self.first_name.lower() < other.first_name.lower()

    def __gt__(self, other):
        return self.first_name.lower() > other.first_name.lower()
    
    def __le__(self, other):
        return self.first_name.lower() <= other.first_name.lower()
    
    def __ge__(self, other):
        return self.first_name.lower() >= other.first_name.lower()

    class Meta:
        managed = False
        db_table = 'USER'

class Timelog(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)  
    user = models.ForeignKey(User, db_column="card_id", on_delete=models.CASCADE)  
    start_time = models.DateTimeField(db_column='START_TIME')  
    end_time = models.DateTimeField(db_column='END_TIME', blank=True, null=True)  
    # delta = end_time-start_time
    
    def delta(self):
        if self.end_time != None:
            return self.end_time - self.start_time

    def __str__(self):
            return "id: " + str(self.id) + \
                    ", start_time: " + str(self.start_time) + \
                    ", end_time: " + str(self.end_time) + \
                    ", <User: " + str(self.user) + ">"
                    
    class Meta:
        managed = False
        db_table = 'TIMELOG'

class Team(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50)
    users = models.ManyToManyField(User, db_column='USERS')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TEAM'