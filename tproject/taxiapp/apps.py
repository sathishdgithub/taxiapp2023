from __future__ import unicode_literals

from django.apps import AppConfig



class TaxiappConfig(AppConfig):
    name = 'taxiapp'
    def ready(self):
        from . import scheduler
        #print("scheduler started")
        scheduler.start()
