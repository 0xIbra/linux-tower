def test_logs_reader_endpoint(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/logs/tail' with log file path
    THEN check that the app returns logs in a list
    """

    with testing_app.test_client() as client:
        uri = '/api/logs/tail?log_file=/var/log/syslog'
        response = client.get(uri, headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'logs' in content
        assert len(content['logs']) == 25


def test_logs_reader_endpoint_with_limit_10(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/logs/tail' with log file path
    THEN check that the app returns a max of 10 logs in a list
    """

    with testing_app.test_client() as client:
        uri = '/api/logs/tail?log_file=/var/log/syslog&lines=10'
        response = client.get(uri, headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is dict
        assert 'logs' in content
        assert len(content['logs']) == 10


def test_logs_reader_endpoint_nonexistent_file(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/logs/tail' with file that does not exist
    THEN check that the app returns a 400 http response
    """

    with testing_app.test_client() as client:
        uri = '/api/logs/tail?log_file=/var/log/doesnotexist.log&lines=10'
        response = client.get(uri, headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 400
        assert type(content) is dict
        assert 'detail' in content
