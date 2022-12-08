from flask import render_template
from entities import Alerts
from helpers.log_inspector import LogInspector
from helpers.shell import service_show, does_service_exist, is_service_running
from api import db
from datetime import datetime
import requests
import os


def alerting_task(*args):
    app = args[0]
    with app.app_context():
        alerts = db.session.query(Alerts).all()
        for alert in alerts:
            if alert.regex is None or alert.regex == '':
                continue

            if alert.alert_type == Alerts.ALERT_TYPE_LOG:
                __handle_log_alert(app, alert)
            elif alert.alert_type == Alerts.ALERT_TYPE_SERVICE:
                __handle_service_alert(app, alert)
            elif alert.alert_type == Alerts.ALERT_TYPE_METRIC:
                __handle_metric_alert(app, alert)


def __handle_log_alert(app, alert):
    if alert.alert_type == 'logfile':
        logfile_path = alert.logfile_path
        webhook_method = alert.webhook_method
        webhook_url = alert.webhook_url

        if not os.path.isfile(logfile_path):
            return False

        log_inspector = LogInspector(logfile_path)
        first_line_checksum = log_inspector.get_first_line_checksum()

        # if first run
        if alert.logfile_first_line_checksum is None and alert.logfile_last_read_line_number is None:
            line_count, last_line_nb, logs = log_inspector.search_regex()
            alert.logfile_first_line_checksum = first_line_checksum
            alert.logfile_last_read_line_number = last_line_nb

            db.session.commit()

            return False

        # if log file has changed (log rotation)
        if alert.logfile_first_line_checksum != first_line_checksum:
            # first log in file is not the same as before
            # probably log file rotated
            alert.logfile_first_line_checksum = first_line_checksum
            alert.logfile_last_read_line_number = 0

        regex = alert.regex
        start_line = alert.logfile_last_read_line_number
        line_count, last_line_nb, detected_error_logs = log_inspector.search_regex(regex, start_line)

        alert.logfile_last_read_line_number = last_line_nb

        if len(detected_error_logs) > 0:
            # detected

            cooldown_time = alert.cooldown_time
            if cooldown_time is None:
                # if cooldown time not defined, set it to 15 minutes be default
                cooldown_time = 15

            if alert.last_triggered_at is not None:
                now = datetime.now()
                minutes = divmod((now - alert.last_triggered_at).total_seconds(), 60)[0]

                if minutes < cooldown_time:
                    db.session.commit()

                    return False

            alert.last_triggered_at = datetime.now()
            db.session.commit()

            hostname = os.uname().nodename
            err_logs_count = len(detected_error_logs)

            available_parameters = {'hostname': hostname, 'number_of_logs': err_logs_count, 'error_logs': detected_error_logs}

            if alert.slack_webhook_url is not None:
                alert_template = render_template('alerts/slack/log_alert.jinja2', **available_parameters)
                slack_message = {'type': 'mrkdwn', 'text': alert_template}
                try:
                    requests.post(url=alert.slack_webhook_url, json=slack_message)
                except Exception as e:
                    app.logger.error(e)

            if alert.discord_webhook_url is not None:
                alert_template = render_template('alerts/discord/log_alert.jinja2', **available_parameters)
                discord_message = {'content': alert_template}
                try:
                    requests.post(url=alert.discord_webhook_url, json=discord_message)
                except Exception as e:
                    app.logger.error(e)

            # TODO: email alert


def __handle_service_alert(app, alert):
    if alert.last_triggered_at is not None:
        now = datetime.now()
        minutes = divmod((now - alert.last_triggered_at).total_seconds(), 60)[0]

        if minutes < alert.cooldown_time:
            db.session.commit()

            return False

    service_data = service_show(alert.service_name)
    is_running = is_service_running(service_data)

    available_parameters = {
        'service_name': app.service_name,
        'service_data': service_data,
        'is_running': is_running
    }

    if is_running is False:
        # service not running, dispatch alert
        alert.last_triggered_at = datetime.now()
        db.session.commit()

        if alert.slack_webhook_url is not None:
            alert_template = render_template('alerts/slack/service_alert.jinja2', **available_parameters)
            slack_msg = {'type': 'mrkdwn', 'text': alert_template}

            try:
                requests.post(url=alert.slack_webhook_url, json=slack_msg)
            except Exception as e:
                app.logger.error(e)

        if alert.discord_webhook_url is not None:
            alert_template = render_template('alerts/discord/service_alert.jinja2', **available_parameters)
            discord_msg = {'content': alert_template}
            try:
                requests.post(url=alert.discord_webhook_url, json=discord_msg)
            except Exception as e:
                app.logger.error(e)

        # TODO: email alert


def __handle_metric_alert(app, alert):
    pass
