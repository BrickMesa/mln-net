import datetime
from django.contrib.auth.models import User
from django.db import models

from mln.models.dynamic.module import Module

from . import DarkflameDBModel

DAY = datetime.timedelta(days=1)

class Accounts(DarkflameDBModel):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=35)
    password = models.TextField()
    gm_level = models.IntegerField()
    locked = models.BooleanField()
    banned = models.BooleanField()
    play_key_id = models.IntegerField()
    created_at = models.DateTimeField()
    mute_expire = models.BigIntegerField()
    
    def configure_abstrated_information(self):
        self.is_authenticated = True # I swear to god, this is right, this is not bodge, well... not too much bodge
        self.modules = Module.objects.all()
        self.username = self.name
        self.is_staff = self.gm_level == 9
        self.is_superuser = self.gm_level == 9
        self.is_active = not (self.banned or self.locked)
        self.last_login = datetime.datetime.now()
        self.date_joined = datetime.datetime.now()
        self.email = ""
    
    class Meta:
        managed = False
        db_table = 'accounts'

    def __str__(self):
        return self.name
    
class ActivityLog(DarkflameDBModel):
    id = models.IntegerField(primary_key=True)
    character_id = models.IntegerField()
    activity = models.IntegerField()
    timestamp = models.BigIntegerField()
    map_id = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'activity_log'