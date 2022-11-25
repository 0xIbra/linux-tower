from helpers import exec_shell, service_show
import os


def is_nginx_installed():
    if not os.path.isdir('/etc/nginx'):
        return False

    output = exec_shell('service nginx status')
    print(output)
    if 'could not be found' in output:
        return False

    return True


def nginx_status():
    return exec_shell('service nginx status')


def nginx_service_show():
    return service_show('nginx')


def nginx_state_details():
    details = nginx_service_show()

    state_data = {
        'id': details['Id'],
        'pid': details['MainPID'],
        'description': details['Description'],
        'state': details['SubState']
    }

    if state_data['state'] == 'running':
        state_data['started_at'] = details['ActiveEnterTimestamp']
        state_data['started_at_timestamp'] = details['ActiveEnterTimestampMonotonic']

    return state_data
