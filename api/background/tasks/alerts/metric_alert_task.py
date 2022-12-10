from flask import render_template
from entities import Alerts
from helpers.metrics import system_metrics
from datetime import datetime
import requests
import os


class MetricAlertTask:

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

        metric_rule = self.__alert.get_metric_rule()
        metric_rule['metric'] = self.__alert.metric_name

        is_rule_valid, metrics_data = MetricAlertTask.__test_metric_rule(metric_rule)
        if is_rule_valid is True:
            self.__alert.last_triggered_at = datetime.now()
            self.__db.session.commit()

            available_parameters = metrics_data
            available_parameters['alert'] = self.__alert
            available_parameters['hostname'] = os.uname().nodename

            if self.__alert.slack_webhook_url is not None:
                alert_template = render_template('alerts/slack/metric_alert.jinja2', **available_parameters)
                slack_msg = {'type': 'mrkdwn', 'text': alert_template}

                try:
                    requests.post(url=self.__alert.slack_webhook_url, json=slack_msg)
                except Exception as e:
                    self.__app.logger.error(e)

            if self.__alert.discord_webhook_url is not None:
                alert_template = render_template('alerts/discord/metric_alert.jinja2', **available_parameters)
                discord_msg = {'content': alert_template}
                try:
                    requests.post(url=self.__alert.discord_webhook_url, json=discord_msg)
                except Exception as e:
                    self.__app.logger.error(e)

            # TODO: email alert

    @staticmethod
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
