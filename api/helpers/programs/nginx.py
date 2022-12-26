from helpers import exec_shell, service_show
from helpers.process_finder import Process
from exceptions import NginxNotRunning
import psutil
import os


class Nginx:
    LABEL = 'nginx'
    SYS_ID = 'nginx'

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

    @staticmethod
    def metrics():
        """
        Calculates and returns the CPU and memory utilization by Nginx server.
        """

        nginx_process = Process(name='nginx')
        used = nginx_process.get_memory_usage()
        total_mem = psutil.virtual_memory().total / 1024 / 1024
        percent = (used / total_mem) * 100

        return {
            'cpu_usage': nginx_process.get_cpu_utilization(),
            'memory': {
                'used': used,
                'total': total_mem,
                'percent': percent
            }
        }
