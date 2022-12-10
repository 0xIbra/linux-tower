from helpers import exec_shell, service_show
import os


class Nginx:

    @staticmethod
    def is_installed():
        if not os.path.isdir('/etc/nginx'):
            return False

        output = exec_shell('service nginx status')
        if 'could not be found' in output:
            return False

        return True

    @staticmethod
    def status():
        return exec_shell('service nginx status')

    @staticmethod
    def service_show():
        return service_show('nginx')

    @staticmethod
    def state_details():
        details = Nginx.service_show()

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
