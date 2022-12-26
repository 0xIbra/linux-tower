from endpoints import CpuMetric, MemoryMetric, DiskMetric
from datetime import datetime


def test_get_cpu_metric_data_endpoint(testing_app, test_database, add_metric_data, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/metrics/cpu'
    THEN app should return a list of cpu metric data
    """

    now = datetime.now()
    # create metrics
    for x in range(3):
        add_metric_data('cpu', value=50, created_at=now)

    with testing_app.test_client() as client:
        response = client.get('/api/metrics/cpu', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is list
        assert len(content) == 3
        assert 'value' in content[0]
        assert content[0]['program'] is None


def test_get_memory_metric_data_endpoint(testing_app, test_database, add_metric_data, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/metrics/memory'
    THEN app should return a list of memory metric data
    """

    now = datetime.now()
    # create metrics
    for x in range(3):
        add_metric_data('memory', value=30, created_at=now)

    with testing_app.test_client() as client:
        response = client.get('/api/metrics/memory', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is list
        assert len(content) == 3
        assert 'value' in content[0]
        assert content[0]['program'] is None


def test_get_disk_metric_data_endpoint(testing_app, test_database, add_metric_data, access_token):
    """
    GIVEN a Flask application configured for testing
    WHEN a GET request is made to '/api/metrics/disk'
    THEN app should return a list of disk metric data
    """

    now = datetime.now()
    # create metrics
    for x in range(3):
        add_metric_data('disk', value=30, created_at=now)

    with testing_app.test_client() as client:
        response = client.get('/api/metrics/disk', headers={'Authorization': access_token})
        content = response.get_json()

        assert response.status_code == 200
        assert type(content) is list
        assert len(content) == 3
        assert 'value' in content[0]
        assert 'program' not in content[0]
