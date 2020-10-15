import os, sys

from celery import Celery

import trading.settings

sys.path.append(os.path.abspath('trading'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trading.settings')
celery_app = Celery('trading')
celery_app.config_from_object('django.conf:settings', namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.beat_schedule = {
    "find_trades": {
        "task": "trading_app.tasks.find_trades",
        "schedule": 30,
    },
}
