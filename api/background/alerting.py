from background.tasks import LogAlertTask
from flask import render_template
from entities import Alerts
from helpers.log_inspector import LogInspector
from helpers.shell import service_show, does_service_exist, is_service_running
from helpers.metrics import system_metrics
from api import db
from datetime import datetime
import requests
import os


def alerting_task(*args):
    app = args[0]
    with app.app_context():
        alerts = db.session.query(Alerts).all()
        for alert in alerts:
            if alert.alert_type == Alerts.ALERT_TYPE_LOG:
                log_alert_task = LogAlertTask(app, db, alert)
                log_alert_task.execute()
            elif alert.alert_type == Alerts.ALERT_TYPE_SERVICE:
                __handle_service_alert(app, alert)
            elif alert.alert_type == Alerts.ALERT_TYPE_METRIC:
                __handle_metric_alert(app, alert)


def __handle_service_alert(app, alert):
    if alert.last_triggered_at is not None:
        now = datetime.now()
        minutes = divmod((now - alert.last_triggered_at).total_seconds(), 60)[0]

        if minutes < alert.cooldown_time:
            return False

    service_data = service_show(alert.service_name)
    is_running = is_service_running(service_data)

    available_parameters = {
        'service_name': alert.service_name,
        'service_data': service_data,
        'hostname': os.uname().nodename,
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
    if alert.last_triggered_at is not None:
        now = datetime.now()
        minutes = divmod((now - alert.last_triggered_at).total_seconds(), 60)[0]

        if minutes < alert.cooldown_time:
            return False

    metric_rule = alert.get_metric_rule()
    metric_rule['metric'] = alert.metric_name

    is_rule_valid, metrics_data = __test_metric_rule(metric_rule)
    if is_rule_valid is True:
        alert.last_triggered_at = datetime.now()
        db.session.commit()

        available_parameters = metrics_data
        available_parameters['alert'] = alert
        available_parameters['hostname'] = os.uname().nodename

        if alert.slack_webhook_url is not None:
            alert_template = render_template('alerts/slack/metric_alert.jinja2', **available_parameters)
            slack_msg = {'type': 'mrkdwn', 'text': alert_template}

            try:
                requests.post(url=alert.slack_webhook_url, json=slack_msg)
            except Exception as e:
                app.logger.error(e)

        if alert.discord_webhook_url is not None:
            alert_template = render_template('alerts/discord/metric_alert.jinja2', **available_parameters)
            discord_msg = {'content': alert_template}
            try:
                requests.post(url=alert.discord_webhook_url, json=discord_msg)
            except Exception as e:
                app.logger.error(e)

        # TODO: email alert


def __test_metric_rule(metric_rule: dict):
    operator = metric_rule['operator']
    metric = metric_rule['metric']
    target_value = metric_rule['target_value']

    system_metric_data = system_metrics()
    if metric == 'cpu_usage':
        current_value = system_metric_data['cpu_usage']
    elif metric == 'disk_percent':
        current_value = system_metric_data['disk']['percent']
    elif metric == 'disk_free':
        current_value = system_metric_data['disk']['free']
    elif metric == 'memory_percent':
        current_value = system_metric_data['memory']['percent']
    else:
        raise Exception(f'Unsupported metric "{metric}".')

    if operator == 'eq':
        result = current_value == target_value
    elif operator == 'gt':
        result = current_value > target_value
    elif operator == 'lt':
        result = current_value < target_value
    elif operator == 'gte':
        result = current_value >= target_value
    elif operator == 'lte':
        result = current_value <= target_value
    else:
        raise Exception(f'Unsupported operator "{operator}".')

    system_metric_data['current_value'] = current_value
    system_metric_data['target_value'] = target_value

    return result, system_metric_data
