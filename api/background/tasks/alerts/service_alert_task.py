from flask import render_template
from entities import Alerts
from helpers.shell import service_show, is_service_running
from datetime import datetime
import requests
import os


class ServiceAlertTask:

    def __init__(self, app, db, alert: Alerts):
        self.__app = app
        self.__db = db
        self.__alert = alert

    def execute(self):
        if self.__alert.last_triggered_at is not None:
            now = datetime.now()
            minutes = divmod((now - self.__alert.last_triggered_at).total_seconds(), 60)[0]

            cooldown_time = self.__alert.cooldown_time
            if cooldown_time is None:
                cooldown_time = 15

            if minutes < cooldown_time:
                return False

        service_data = service_show(self.__alert.service_name)
        is_running = is_service_running(service_data)

        available_parameters = {
            'service_name': self.__alert.service_name,
            'service_data': service_data,
            'hostname': os.uname().nodename,
            'is_running': is_running
        }

        if is_running is False:
            # service not running, dispatch alert
            self.__alert.last_triggered_at = datetime.now()
            self.__db.session.commit()

            if self.__alert.slack_webhook_url is not None:
                alert_template = render_template('alerts/slack/service_alert.jinja2', **available_parameters)
                slack_msg = {'type': 'mrkdwn', 'text': alert_template}

                try:
                    requests.post(url=self.__alert.slack_webhook_url, json=slack_msg)
                except Exception as e:
                    self.__app.logger.error(e)

            if self.__alert.discord_webhook_url is not None:
                alert_template = render_template('alerts/discord/service_alert.jinja2', **available_parameters)
                discord_msg = {'content': alert_template}
                try:
                    requests.post(url=self.__alert.discord_webhook_url, json=discord_msg)
                except Exception as e:
                    self.__app.logger.error(e)

            # TODO: email alert
