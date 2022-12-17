from helpers.metrics import system_metrics


def test_system_metrics():
    """
    GIVEN a 'system_metrics' function that returns the system metrics like cpu usage, disk space, etc...
    WHEN 'system_metrics' function is called
    THEN check that the returned value is dict and contains cpu usage, disk and memory information
    """

    metrics = system_metrics()

    assert type(metrics) is dict
    assert 'cpu_usage' in metrics
    assert 'memory' in metrics
    assert 'percent' in metrics['memory']
    assert 'disk' in metrics
    assert 'percent' in metrics['disk']

    memory_percent = metrics['memory']['percent']
    assert memory_percent > 0.0

    disk_percent = metrics['disk']['percent']
    assert disk_percent > 0.0
