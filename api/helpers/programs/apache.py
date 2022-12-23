from helpers import exec_shell, service_show
from exceptions import ApacheNotRunning
import psutil
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

    @staticmethod
    def metrics():
        if not Apache.is_installed():
            raise Exception('Apache is not installed on this server.')

        details = Apache.state_details()
        if details['state'] != 'running':
            raise ApacheNotRunning('Apache is not currently running.')

        main_pid = None
        for p in psutil.process_iter():
            if p.name() != 'apache2':
                continue

            if main_pid is None:
                main_pid = p.pid
            else:
                if p.pid < main_pid:
                    main_pid = p.pid

        cpu_percentages = []
        cpu_utilization = 0
        memory_used = 0
        if main_pid is not None:
            main_process = psutil.Process(main_pid)
            for child_process in main_process.children():
                cpu_percentages.append(child_process.cpu_percent(interval=0.5))
                memory_used += child_process.memory_info().rss

            cpu_utilization = sum(cpu_percentages) / psutil.cpu_count()

        return {
            'cpu_usage': cpu_utilization,
            'memory': {
                'used': memory_used / 1024 / 1024,
                'total': psutil.virtual_memory().total / 1024 / 1024
            }
        }
