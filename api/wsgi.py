from api import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit


app = create_app()

if __name__ == '__main__':
    from background.alerting import alerting_task
    from background.metrics_collection import metrics_collection

    scheduler = BackgroundScheduler()
    scheduler.add_job(id='alerting', func=alerting_task, args=[app], trigger=CronTrigger.from_crontab('*/5 * * * *'))
    scheduler.add_job(id='metrics_collection', func=metrics_collection, args=[app], trigger=CronTrigger.from_crontab('*/15 * * * *'))
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    app.run(host='0.0.0.0', port=9999)
