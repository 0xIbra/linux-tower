from helpers.shell import service_show, does_service_exist, is_service_running, exec_shell


def test_service_show():
    data = service_show('apache2')

    assert type(data) is dict
    assert 'SubState' in data


def test_does_service_exist():
    data = service_show('apache2')
    result_true = does_service_exist(data)
    result_false = does_service_exist({'LoadError': True})

    assert result_true is True
    assert result_false is False


def test_is_service_running():
    data = service_show('apache2')
    running = is_service_running(data)

    assert running is True


def test_exec_shell():
    output = exec_shell('service nginx status')

    assert 'nginx.service could not be found.' in output
