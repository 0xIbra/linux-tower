from math import floor
import psutil
import os


def system_metrics():
    payload = {
        'cpu_usage': psutil.cpu_percent(4),
    }

    mem_stats = psutil.virtual_memory()
    payload['memory'] = {
        'percent': mem_stats.percent,
        'total': floor(mem_stats.total / (1024 * 1024)),
        'available': floor(mem_stats.available / (1024 * 1024)),
        'used': floor(mem_stats.used / (1024 * 1024)),
        'free': floor(mem_stats.free / (1024 * 1024)),
        'active': floor(mem_stats.active / (1024 * 1024)),
        'inactive': floor(mem_stats.inactive / (1024 * 1024)),
        'buffers': floor(mem_stats.buffers / (1024 * 1024)),
        'cached': floor(mem_stats.cached / (1024 * 1024)),
        'shared': floor(mem_stats.shared / (1024 * 1024)),
        'slab': floor(mem_stats.slab / (1024 * 1024))
    }

    disk_stats = psutil.disk_usage(os.sep)
    payload['disk'] = {
        'percent': disk_stats.percent,
        'total': round((disk_stats.total / (1024 * 1024)) / 1000, 2),
        'used': round((disk_stats.used / (1024 * 1024)) / 1000, 2),
        'free': round((disk_stats.free / (1024 * 1024)) / 1000, 2),
    }

    return payload
