import os

LOG_LINE = '[Tue Dec 13 07:18:04.916767 2022] [mpm_prefork:notice] [pid 10848] AH00163: Apache/2.4.41 (Ubuntu) configured -- resuming normal operations'
LOG_FILE = '/tmp/pytest_mock.log'


def create_log_file():
    with open(LOG_FILE, 'w') as f:
        for i in range(100):
            line = f'{LOG_LINE} - {i+1}' + '\n'
            f.write(line)


def delete_log_file():
    if os.path.isfile(LOG_FILE):
        os.remove(LOG_FILE)
