import psutil


def processes_info():
    payload = []
    for proc in psutil.process_iter(['pid', 'username', 'name']):
        proc.cpu_percent()
        cpu_usage = proc.cpu_percent(interval=0.1)
        if cpu_usage > 0.0:
            cpu_usage = cpu_usage / psutil.cpu_count()
        else:
            cpu_usage = None

        payload.append({
            'name': proc.name(),
            'pid': proc.pid,
            'user': proc.username(),
            'usage': {
                'cpu': cpu_usage
            }
        })

    return payload
