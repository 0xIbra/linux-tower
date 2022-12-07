import subprocess


def exec_shell(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (result, error) = proc.communicate()
    result = result.decode('utf8').strip()
    error = error.decode('utf8').strip()

    if error == '':
        output = result
    else:
        output = error

    return output


def service_show(service_name):
    formatted = {}
    output = exec_shell(f'systemctl show {service_name} --no-page')
    output = output.split('\n')
    for line in output:
        key, value = line.split('=', maxsplit=1)
        formatted[key] = value

    return formatted


def does_service_exist(service_data):
    if 'LoadError' in service_data:
        return False

    return True


def is_service_running(service_state_data):
    return service_state_data['SubState'] == 'running'
