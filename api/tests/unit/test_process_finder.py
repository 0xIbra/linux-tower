from helpers.process_finder import Process
from exceptions import ProcessNotFound
import pytest

def test_process():
    """
    GIVEN a 'Process' class that retrieves `psutil.Process` instance
    WHEN class instantiated
    THEN check that no exception is thrown
    """

    pytest_process = Process(name='pytest')


def test_process_not_found():
    """
    GIVEN a 'Process' class that retrieves `psutil.Process` instance
    WHEN class instantiated with invalid process name
    THEN check that `ProcessNotFound` exception is thrown
    """

    with pytest.raises(ProcessNotFound) as e:
        process = Process(name='not_real_process')


def test_process_cpu_utilization():
    """
    GIVEN a 'Process' class that retrieves `psutil.Process` instance
    WHEN 'cpu_utilization' method is called
    THEN check that the returned value is numeric (positive)
    """

    process = Process(name='pytest')
    usage = process.get_cpu_utilization()

    assert type(usage) is int or type(usage) is float


def test_process_memory_usage():
    """
    GIVEN a 'Process' class that retrieves `psutil.Process` instance
    WHEN 'memory_usage' method is called
    THEN check that the returned value is numeric (positive)
    """

    process = Process(name='pytest')
    usage = process.get_memory_usage()

    assert type(usage) is int or type(usage) is float
    assert usage > 0
