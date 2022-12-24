from helpers.programs import MySQL
from exceptions import ProcessNotFound
import pytest


def test_is_installed():
    """
    GIVEN a 'MySQL' class that groups together methods relevant to the MySQL systemd service
    WHEN 'is_installed' method is called
    THEN check that the returned value is True
    """

    is_installed = MySQL.is_installed()
    assert is_installed is True


def test_status():
    """
    GIVEN a 'MySQL' class that groups together methods relevant to the MySQL systemd service
    WHEN 'status' method is called
    THEN check that the returned value contains text stating mysql is running
    """

    status = MySQL.status()
    assert type(status) is str
    assert 'active (running) since' in status


def test_service_show():
    """
    GIVEN a 'MySQL' class that groups together methods relevant to the MySQL systemd service
    WHEN 'service_show' method is called
    THEN check that the returned value is dict type and contains relevant information
    """

    service_data = MySQL.service_show()
    assert type(service_data) is dict
    assert 'SubState' in service_data
    assert service_data['SubState'] == 'running'


def test_state_details():
    """
    GIVEN a 'MySQL' class that groups together methods relevant to the MySQL systemd service
    WHEN 'state_details' method is called
    THEN check that the returned value is dict type and contains formatted data
    """

    state_details = MySQL.state_details()
    assert type(state_details) is dict
    assert 'id' in state_details
    assert 'description' in state_details
    assert state_details['state'] == 'running'
    assert 'started_at' in state_details


def test_metrics_expect_exception():
    """
    GIVEN a 'MySQL' class that groups together methods relevant to the MySQL systemd service
    WHEN 'metrics' method is called
    THEN expect an exception as there is not a real MySQL server running on the machine.
    """

    with pytest.raises(ProcessNotFound) as e:
        MySQL.metrics()
