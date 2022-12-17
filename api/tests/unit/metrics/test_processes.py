from helpers.metrics import processes_info


def test_processes_info():
    """
    GIVEN a 'processes_info' function that returns information about all currently running processes on the system
    WHEN 'processes_info' function is called
    THEN check that the returned value is dict and contains relevant linux processes with relevant info
    """

    processes = processes_info()
    assert type(processes) is list
    assert len(processes) > 0

    systemd_process = next(x for x in processes if x["name"] == 'python')
    assert systemd_process is not None
    assert 'pid' in systemd_process
    assert systemd_process['is_running'] is True
