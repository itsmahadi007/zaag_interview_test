# settings/celery.py
from celery.schedules import crontab

CELERY_TIMEZONE = "Asia/Dhaka"

CELERY_BEAT_SCHEDULE = {

    "mail_blasting": {
        "task": "apps.notification_management.tasks.mail_blast",
        "schedule": crontab(hour="*/3"),
    },

}
