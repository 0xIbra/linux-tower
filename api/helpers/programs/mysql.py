from helpers import exec_shell, service_show
from helpers.process_finder import Process
import psutil


class MySQL:

    @staticmethod
    def is_installed():
        output = exec_shell('service mysql status')
        if 'could not be found' in output:
            return False

        return True

    @staticmethod
    def status():
        return exec_shell('service mysql status')

    @staticmethod
    def service_show():
        return service_show('mysql')

    @staticmethod
    def state_details():
        details = MySQL.service_show()

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

    @staticmethod
    def metrics():
        """
        Calculates and returns the CPU and memory utilization by MySQL server.
        """

        apache_process = Process(name='mysqld')
        total_mem = psutil.virtual_memory().total / 1024 / 1024

        return {
            'cpu_usage': apache_process.get_cpu_utilization(),
            'memory': {
                'used': apache_process.get_memory_usage(),
                'total': total_mem
            }
        }
