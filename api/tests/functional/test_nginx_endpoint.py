def test_nginx_endpoint(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/nginx/status'
    THEN check that nginx state data is returned with a 200 http response
    """

    with testing_app.test_client() as client:
        response = client.get('/api/nginx/status', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 404
        assert response.headers.get('content-type') == 'application/json'
        assert type(content) is dict
        assert 'detail' in content
        assert 'does not seem to be installed' in content['detail']
