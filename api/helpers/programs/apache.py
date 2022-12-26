from helpers import exec_shell, service_show
from helpers.process_finder import Process
from exceptions import ApacheNotRunning
import psutil
import os


class Apache:
    LABEL = 'apache2'
    SYS_ID = 'apache2'

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

    @staticmethod
    def metrics():
        """
        Calculates and returns the CPU and memory utilization by Apache server.
        """

        apache_process = Process(name='apache2')
        used = apache_process.get_memory_usage()
        total_mem = psutil.virtual_memory().total / 1024 / 1024
        percent = (used / total_mem) * 100

        return {
            'cpu_usage': apache_process.get_cpu_utilization(),
            'memory': {
                'used': used,
                'total': total_mem,
                'percent': percent
            }
        }
