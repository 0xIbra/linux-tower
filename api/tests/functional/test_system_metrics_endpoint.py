def test_system_metrics_endpoint(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/system_metrics'
    THEN check that system metrics are returned with a 200 http response
    """

    with testing_app.test_client() as client:
        response = client.get('/api/system_metrics', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert type(content) is dict
        assert 'cpu_usage' in content


def test_system_metrics_endpoint_without_credentials(testing_app):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/system_metrics' without access token
    THEN check that app returns a 401 http response
    """

    with testing_app.test_client() as client:
        response = client.get('/api/system_metrics')
        content = response.get_json()

        assert response.status_code == 401
        assert type(content) is dict
        assert 'detail' in content
        assert 'token not found in request' in content['detail']

        response = client.get('/api/system_metrics', headers={'Authorization': 'faketoken'})
        content = response.get_json()

        assert response.status_code == 401
        assert 'token is invalid' in content['detail']
