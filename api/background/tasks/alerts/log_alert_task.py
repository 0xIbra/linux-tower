from flask import render_template
from entities import Alerts
from helpers.log_inspector import LogInspector
from datetime import datetime
import requests
import os


class LogAlertTask:

    def __init__(self, app, db, alert: Alerts):
        self.__app = app
        self.__db = db
        self.__alert = alert

    def execute(self):
        logfile_path = self.__alert.logfile_path
        webhook_method = self.__alert.webhook_method
        webhook_url = self.__alert.webhook_url

        if not os.path.isfile(logfile_path):
            return False

        log_inspector = LogInspector(logfile_path)
        first_line_checksum = log_inspector.get_first_line_checksum()

        # if first run
        if self.__alert.logfile_first_line_checksum is None and self.__alert.logfile_last_read_line_number is None:
            line_count, last_line_nb, logs = log_inspector.search_regex()
            self.__alert.logfile_first_line_checksum = first_line_checksum
            self.__alert.logfile_last_read_line_number = last_line_nb

            self.__db.session.commit()

            return False

        # if log file has changed (log rotation)
        if self.__alert.logfile_first_line_checksum != first_line_checksum:
            # first log in file is not the same as before
            # probably log file rotated
            self.__alert.logfile_first_line_checksum = first_line_checksum
            self.__alert.logfile_last_read_line_number = 0

        regex = self.__alert.regex
        start_line = self.__alert.logfile_last_read_line_number
        line_count, last_line_nb, detected_error_logs = log_inspector.search_regex(regex, start_line)

        self.__alert.logfile_last_read_line_number = last_line_nb

        if len(detected_error_logs) > 0:
            # detected

            cooldown_time = self.__alert.cooldown_time
            if cooldown_time is None:
                # if cooldown time not defined, set it to 15 minutes be default
                cooldown_time = 15

            if self.__alert.last_triggered_at is not None and cooldown_time is not None:
                now = datetime.now()
                minutes = divmod((now - self.__alert.last_triggered_at).total_seconds(), 60)[0]

                if minutes < cooldown_time:
                    self.__db.session.commit()

                    return False

            self.__alert.last_triggered_at = datetime.now()
            self.__db.session.commit()

            hostname = os.uname().nodename
            err_logs_count = len(detected_error_logs)

            available_parameters = {'hostname': hostname, 'number_of_logs': err_logs_count,
                                    'error_logs': detected_error_logs}

            if self.__alert.slack_webhook_url is not None:
                alert_template = render_template('alerts/slack/log_alert.jinja2', **available_parameters)
                slack_message = {'type': 'mrkdwn', 'text': alert_template}
                try:
                    requests.post(url=self.__alert.slack_webhook_url, json=slack_message)
                except Exception as e:
                    self.__app.logger.error(e)

            if self.__alert.discord_webhook_url is not None:
                alert_template = render_template('alerts/discord/log_alert.jinja2', **available_parameters)
                discord_message = {'content': alert_template}
                try:
                    requests.post(url=self.__alert.discord_webhook_url, json=discord_message)
                except Exception as e:
                    self.__app.logger.error(e)

            # TODO: email alert
