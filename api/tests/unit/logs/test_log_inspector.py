import pytest

from helpers.log_inspector import LogInspector
from tests.unit.logs import create_log_file, delete_log_file, LOG_FILE, LOG_LINE
from hashlib import md5


def test_log_inspector_search_ok():
    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', return_limit=200)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 100

    delete_log_file()


def test_log_inspector_search_limited():
    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', return_limit=10)

    assert line_count == 11
    assert last_line == 10
    assert type(found) is list
    assert len(found) == 10

    delete_log_file()


def test_log_inspector_search_with_start_line():
    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='mpm_prefork', start_line=50, return_limit=100)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 50

    delete_log_file()


def test_log_inspector_search_last_line():
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
    create_log_file()

    inspector = LogInspector(LOG_FILE)
    line_count, last_line, found = inspector.search_regex(regex='notfound', return_limit=200)

    assert line_count == 100
    assert last_line == 99
    assert type(found) is list
    assert len(found) == 0

    delete_log_file()


def test_log_inspector_check_first_line_checksum():
    create_log_file()

    inspector = LogInspector(LOG_FILE)
    checksum = inspector.get_first_line_checksum()
    expected = md5(str(LOG_LINE + ' - 1').encode('utf8')).hexdigest()

    assert type(checksum) is str
    assert checksum == expected

    delete_log_file()


def test_log_inspector_search_error():
    with pytest.raises(Exception) as e:
        LogInspector('/file/does/not/exist.log')

    assert 'file was not found.' in str(e.value)
