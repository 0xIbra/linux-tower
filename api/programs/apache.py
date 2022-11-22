from helpers import exec_shell
import os


def is_apache_installed():
    if not os.path.isdir('/etc/apache2'):
        return False

    output = exec_shell('service apache2 status')
    if 'could not be found' in output:
        return False

    return True
