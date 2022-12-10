from helpers import exec_shell, service_show
import os


class Apache:

    @staticmethod
    def is_installed():
        if not os.path.isdir('/etc/apache2'):
            return False

        output = exec_shell('service apache2 status')
        if 'could not be found' in output:
            return False

        return True

    @staticmethod
    def status():
        return exec_shell('service apache2 status')

    @staticmethod
    def service_show():
        return service_show('apache2')

    @staticmethod
    def state_details():
        details = Apache.service_show()

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
