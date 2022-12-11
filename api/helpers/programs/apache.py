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

    @staticmethod
    def list_vhosts():
        vhost_dir = '/etc/apache2/sites-enabled'
        vhosts = []
        file_list = os.listdir(vhost_dir)
        for file in file_list:
            vhost = {'file': file}
            with open(os.path.join(vhost_dir, file)) as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if line == '':
                        continue
                    if 'VirtualHost' in line:
                        continue
                    if line[0] == '#':
                        continue
                    if 'ServerName' not in line and 'ServerAlias' not in line:
                        continue

                    values = line.split(' ')
                    if len(values) > 2:
                        name = values[0]
                        value = values[1:]
                    elif len(values) == 1:
                        continue
                    else:
                        name, value = values[0], values[1]
                        name = name.strip()
                        value = value.strip()

                    name = name.replace('<', '')
                    name = name.replace('>', '')

                    vhost[name] = value

            vhosts.append(vhost)

        return vhosts
