from api import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = create_app()


if __name__ == '__main__':
    from background.alerting import alerting_task

    scheduler = BackgroundScheduler()
    scheduler.add_job(id='alerting', func=alerting_task, args=[app], trigger='interval', seconds=10)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    app.run(host='0.0.0.0', port=9999)
