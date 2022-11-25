import psutil


def processes_info(with_cpu_usage=False):
    payload = []
    for proc in psutil.process_iter(['pid', 'username', 'name']):
        cpu_usage = None
        if with_cpu_usage is True:
            proc.cpu_percent()
            cpu_usage = proc.cpu_percent(interval=0.1)
            if cpu_usage > 0.0:
                cpu_usage = cpu_usage / psutil.cpu_count()

        payload.append({
            'name': proc.name(),
            'pid': proc.pid,
            'user': proc.username(),
            'status': proc.status(),
            'is_running': proc.is_running(),
            'created_at': proc.create_time(),
            'usage': {
                'cpu': cpu_usage,
                'memory': {
                    'percent': round(proc.memory_percent(), 2),
                    'rss': proc.memory_info().rss / (1024 * 1024)
                }
            }
        })

    if with_cpu_usage is True:
        payload.sort(key=lambda e: e['usage']['cpu'], reverse=True)
    else:
        payload.sort(key=lambda e: e['usage']['memory']['rss'], reverse=True)

    return payload
