from helpers.programs import Nginx
from exceptions import NginxNotRunning
import pytest

def test_is_installed():
    """
    GIVEN a 'Nginx' class that groups together methods relevant to the Nginx systemd service
    WHEN 'is_installed' method is called
    THEN check that the returned value is true
    """

    is_installed = Nginx.is_installed()
    assert is_installed is False


def test_status():
    """
    GIVEN a 'Nginx' class that groups together methods relevant to the Nginx systemd service
    WHEN 'status' method is called
    THEN check that the returned value contains text saying nginx was not found
    """

    status = Nginx.status()
    assert type(status) is str
    assert 'could not be found' in status


def test_service_show():
    """
    GIVEN a 'Nginx' class that groups together methods relevant to the Nginx systemd service
    WHEN 'service_show' method is called
    THEN check that the returned value is dict and contains relevant information
    """

    service_data = Nginx.service_show()
    assert type(service_data) is dict
    assert 'SubState' in service_data
    assert service_data['SubState'] == 'dead'
    assert 'LoadError' in service_data
    assert 'nginx.service not found' in service_data['LoadError']


def test_state_details():
    """
    GIVEN a 'Nginx' class that groups together methods relevant to the Nginx systemd service
    WHEN 'state_details' method is called
    THEN check that the returned value is dict and contains formatted data
    """

    state_details = Nginx.state_details()
    assert type(state_details) is dict
    assert state_details['state'] == 'dead'
    assert 'started_at' not in state_details


def test_metrics():
    """
    GIVEN a 'Nginx' class that groups together methods relevant to the Nginx systemd service
    WHEN 'metrics' method is called
    THEN check that the returned payload contains relevant info on system resource utilization
    """

    metrics = Nginx.metrics()
    assert type(metrics) is dict
    assert 'cpu_usage' in metrics
    assert 'memory' in metrics
    assert metrics['memory']['total'] > 0
