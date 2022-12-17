def test_apache_endpoint(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/apache/status'
    THEN check that apache state data is returned with a 200 http response
    """

    with testing_app.test_client() as client:
        response = client.get('/api/apache/status', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert type(content) is dict
        assert 'data' in content
        assert 'status' in content['data']
        assert 'details' in content['data']
        assert content['data']['details']['state'] == 'running'
