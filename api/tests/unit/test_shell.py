from helpers.shell import service_show, does_service_exist, is_service_running, exec_shell


def test_service_show():
    """
    GIVEN a 'service_show' function that executes a specific shell command
    WHEN function is called with 'apache2' as required parameter
    THEN check that the returned result contains relevant information like 'SubState'
    """

    data = service_show('apache2')

    assert type(data) is dict
    assert 'SubState' in data


def test_does_service_exist():
    """
    GIVEN a 'service_show' function and 'does_service_exist' function that execute specific shell commands
    WHEN 'does_service_exist' is called with necessary params
    THEN check that the returned result is true
    """

    data = service_show('apache2')
    result_true = does_service_exist(data)
    result_false = does_service_exist({'LoadError': True})

    assert result_true is True
    assert result_false is False


def test_is_service_running():
    """
    GIVEN a 'is_service_running' function that executes a specific shell command
    WHEN function is called with 'apache2' as required parameter
    THEN check that the returned result is True
    """

    data = service_show('apache2')
    running = is_service_running(data)

    assert running is True


def test_exec_shell():
    """
    GIVEN a 'exec_shell' function that executes given shell command
    WHEN function is called with the 'service apache2 status' command
    THEN check that the returned result checks out
    """

    output = exec_shell('service nginx status')

    assert 'nginx.service could not be found.' in output
