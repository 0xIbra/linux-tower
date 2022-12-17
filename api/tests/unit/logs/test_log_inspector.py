import pytest

from helpers.log_inspector import LogInspector
from tests.unit.logs import create_log_file, delete_log_file, LOG_FILE, LOG_LINE
from hashlib import md5


def test_log_inspector_search_ok():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN the 'search_regex' method is called with $regex as param and $return_limit
    THEN check that the searched term is found in returned result
    """

    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', return_limit=200)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 100

    delete_log_file()


def test_log_inspector_search_limited():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN the 'search_regex' method is called with $regex as param and $return_limit
    THEN check that the returned result is limited to defined limit with $return_limit param
    """

    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', return_limit=10)

    assert line_count == 11
    assert last_line == 10
    assert type(found) is list
    assert len(found) == 10

    delete_log_file()


def test_log_inspector_search_with_start_line():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN the 'search_regex' method is called with $regex as param, $start_line and $return_limit
    THEN check that the returned result contains lines starting from defined line $start_line param and not before
    """

    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', start_line=50, return_limit=100)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 50

    delete_log_file()


def test_log_inspector_search_last_line():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN the 'search_regex' method is called with $regex as param and $start_line as last line of file
    THEN check that only 1 line is returned
    """

    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', start_line=99)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 1
    assert found[0]['line'] == 99
    assert found[0]['log'].endswith('- 100')

    delete_log_file()


def test_log_inspector_search_not_ok():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN the 'search_regex' method is called with $regex param containing a term that is not in the file
    THEN check that empty result is returned
    """

    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='notfound', return_limit=200)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 0

    delete_log_file()


def test_log_inspector_check_first_line_checksum():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN the 'get_first_line_checksum' method is called
    THEN check that the returned value is a md5 hash of the first line of the file
    """

    create_log_file()

    inspector = LogInspector(LOG_FILE)
    checksum = inspector.get_first_line_checksum()
    expected = md5(str(LOG_LINE + ' - 1').encode('utf8')).hexdigest()

    assert type(checksum) is str
    assert checksum == expected

    delete_log_file()


def test_log_inspector_search_error():
    """
    GIVEN a LogInspector component that reads .log files
    WHEN an instance is instantiated with non-existing file as parameter
    THEN check that the component raises an 'Exception'
    """

    with pytest.raises(Exception) as e:
        LogInspector('/file/does/not/exist.log')

    assert 'file was not found.' in str(e.value)
