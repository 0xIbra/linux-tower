import subprocess


def exec_shell(command):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (result, error) = proc.communicate()
    result = result.decode('utf8').strip()
    error = error.decode('utf8').strip()

    if error == '':
        output = result
    else:
        output = error

    return output
