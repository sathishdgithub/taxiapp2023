from apscheduler.schedulers.background import BackgroundScheduler
from .views import SendSMS_Owner_Driver

def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(SendSMS_Owner_Driver,'interval',minutes=5)
    scheduler.add_job(SendSMS_Owner_Driver,'cron',day=18,hour=2,minute=30)
    scheduler.start()
