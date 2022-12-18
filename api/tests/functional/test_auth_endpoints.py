def test_authentication_endpoint(testing_app):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/auth' with valid credentials
    THEN check that the authentication with pam is accepted and JWT token is returned 200 http response
    """

    with testing_app.test_client() as client:
        payload = {
            'username': 'linuxtower',
            'password': 'linuxtower'
        }
        response = client.post('/api/auth', json=payload)
        content = response.get_json()

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert type(content) is dict
        assert 'access_token' in content


def test_authentication_endpoint_with_invalid_credentials(testing_app):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/auth' with invalid credentials
    THEN check that the authentication fails and a 401 http response is returned
    """

    with testing_app.test_client() as client:
        payload = {
            'username': 'fake',
            'password': 'wrong'
        }
        response = client.post('/api/auth', json=payload)
        content = response.get_json()

        assert response.status_code == 401
        assert 'credentials invalid' in content['detail']


def test_authentication_endpoint_without_credentials(testing_app):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request is made to '/api/auth' without credentials
    THEN check that the authentication fails and a 401 http response is returned
    """

    with testing_app.test_client() as client:
        response = client.post('/api/auth', json={})
        content = response.get_json()

        assert response.status_code == 400
        assert type(content) is dict
        assert 'please provide' in content['detail']
