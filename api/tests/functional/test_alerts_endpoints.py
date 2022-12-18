from entities import Alerts


def test_get_alerts_endpoint(testing_app, test_database, add_alert, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/alerts'
    THEN app should return a list of alerts
    """

    add_alert(
        alert_type=Alerts.ALERT_TYPE_LOG,
        regex='error',
        logfile_path='/opt/src/logs/error.log'
    )

    with testing_app.test_client() as client:
        response = client.get('/api/alerts', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is list
        assert len(content) > 0
        assert content[0]['logfile_path'] == '/opt/src/logs/error.log'


def test_get_alert_by_id_endpoint(testing_app, test_database, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/alerts/<id>' with an ID
    THEN app should return the alert with provided ID
    """

    with testing_app.test_client() as client:
        response = client.get('/api/alerts/1', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'id' in content
        assert content['logfile_path'] == '/opt/src/logs/error.log'


def test_create_alerts_endpoint(testing_app, test_database, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/alerts' with json data
    THEN app should create the alert and return 200 response
    """

    # metric type alert
    with testing_app.test_client() as client:
        payload = {
            'alert_type': Alerts.ALERT_TYPE_METRIC,
            'metric_name': Alerts.CPU_METRIC,
            'metric_rule': {'metric': 'cpu_usage', 'operator': 'gte', 'target_value': 90},
            'webhook_method': 'POST',
            'webhook_url': 'https://mywebhook.local/api/hook',
            'slack_webhook_url': 'https://myslack.local/channel/hook',
            'discord_webhook_url': 'https://mydiscord.local/channel/hook'
        }
        headers = {'Authorization': access_token}

        response = client.post('/api/alerts', headers=headers, json=payload)
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'successful' in content['detail']

    # log type alert
    with testing_app.test_client() as client:
        payload = {
            'alert_type': Alerts.ALERT_TYPE_LOG,
            'regex': 'error',
            'logfile_path': '/opt/src/logs/anotherfile.log',
            'webhook_method': 'POST',
            'webhook_url': 'https://mywebhook.local/api/hook',
            'slack_webhook_url': 'https://myslack.local/channel/hook',
            'discord_webhook_url': 'https://mydiscord.local/channel/hook'
        }
        headers = {'Authorization': access_token}

        response = client.post('/api/alerts', headers=headers, json=payload)
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'successful' in content['detail']

    # service type alert
    with testing_app.test_client() as client:
        payload = {
            'alert_type': Alerts.ALERT_TYPE_SERVICE,
            'service_name': 'apache2',
            'cooldown_time': 30,
            'webhook_method': 'POST',
            'webhook_url': 'https://mywebhook.local/api/hook',
            'slack_webhook_url': 'https://myslack.local/channel/hook',
            'discord_webhook_url': 'https://mydiscord.local/channel/hook'
        }
        headers = {'Authorization': access_token}

        response = client.post('/api/alerts', headers=headers, json=payload)
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'successful' in content['detail']


def test_update_alert_endpoint(testing_app, test_database, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a PUT request is made to '/api/alerts/<id>' with an ID and json data to update
    THEN app should save changes to db and return 200 http response
    """

    with testing_app.test_client() as client:
        payload = {
            'logfile_path': '/opt/app/logs/error.log',
            'cooldown_time': 30,
            'regex': 'error|critical',
            'webhook_method': 'POST',
            'webhook_url': 'https://mywebhook.local/api/hook',
            'slack_webhook_url': 'https://myslack.local/channel/hook',
            'discord_webhook_url': 'https://mydiscord.local/channel/hook'
        }
        response = client.put('/api/alerts/1', headers={'Authorization': access_token}, json=payload)
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'detail' in content
        assert 'updated successfully' in content['detail']


def test_delete_alert_endpoint(testing_app, test_database, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a DELETE request is made to '/api/alerts/<id>' with an ID
    THEN app should delete the alert from db and return 200 http response
    """

    with testing_app.test_client() as client:
        response = client.get('/api/alerts', headers={'Authorization': access_token})
        content = response.get_json()

        # count
        assert response.status_code == 200
        assert type(content) is list
        assert len(content) == 4

        # delete
        for id in range(1, 5):
            response = client.delete(f'/api/alerts/{id}', headers={'Authorization': access_token})
            assert response.status_code == 200

        # count again
        response = client.get('/api/alerts', headers={'Authorization': access_token})
        content = response.get_json()
        assert response.status_code == 200
        assert type(content) is list
        assert len(content) == 0

