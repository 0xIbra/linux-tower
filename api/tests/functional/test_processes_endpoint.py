def test_processes_endpoint(testing_app, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/processes'
    THEN check that currently running processes are returned with a 200 http response
    """

    with testing_app.test_client() as client:
        headers = {'Authorization': access_token}
        response = client.get('/api/processes?cpu_usage=true', headers=headers)
        content = response.get_json()

        assert response.status_code == 200
        assert response.headers.get('content-type') == 'application/json'
        assert type(content) is list
        assert len(content) > 0
        assert 'name' in content[0]
        assert 'status' in content[0]
