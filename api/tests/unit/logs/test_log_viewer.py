from helpers.log_viewer import LogViewer
from tests.unit.logs import create_log_file, delete_log_file, LOG_FILE, LOG_LINE


def test_read_first_non_null_line():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'read_first_non_null_line' method is called
    THEN check that the result is valid by comparing the returned log line, it should be the first line of the file
    """

    create_log_file()

    viewer = LogViewer(LOG_FILE)
    line = viewer.read_first_non_null_line()

    assert type(line) is str
    assert line == (LOG_LINE + ' - 1')

    delete_log_file()


def test_read_last_non_null_line():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'read_last_non_null_line' method is called
    THEN check that the returned value is the last log (last line) in the log file
    """

    create_log_file()

    viewer = LogViewer(LOG_FILE)
    line = viewer.read_last_non_null_line()

    assert type(line) is str
    assert line == (LOG_LINE + ' - 100')

    delete_log_file()


def test_head():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'head' method is called
    THEN check that the returned result is x number of first lines of file
    """

    create_log_file()

    viewer = LogViewer(LOG_FILE)
    head = viewer.head(10)

    expected = []
    for i in range(10):
        line = f'{LOG_LINE} - {str(i + 1)}'
        expected.append(line)

    assert type(head) is list
    assert len(head) == 10
    assert expected == head

    delete_log_file()


def test_tail():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'tail' method is called
    THEN check that the returned result is x number of lines starting from the bottom of the log file
    """

    create_log_file()

    viewer = LogViewer(LOG_FILE)
    tail = viewer.tail(10)

    expected = []
    for i in range(91, 101):
        expected.append(f'{LOG_LINE} - {i}')

    # expected.reverse()

    assert type(tail) is list
    assert expected == tail

    delete_log_file()


def test_readall():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'readall' method is called
    THEN check that the returned result is all the lines of the log file
    """

    create_log_file()

    viewer = LogViewer(LOG_FILE)
    all_lines = viewer.readall()

    expected = []
    for i in range(1, 101):
        expected.append(f'{LOG_LINE} - {i}')

    assert type(all_lines) is list
    assert len(all_lines) == 100
    assert all_lines == expected

    delete_log_file()


def test_read():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'read' method is called with $start and $end parameters
    THEN check that the returned result is lines from file starting from $start line and ending at $end
    """

    create_log_file()

    viewer = LogViewer(LOG_FILE)
    lines, from_line, to_line = viewer.read(0, 9)

    expected = []
    for i in range(1, 11):
        expected.append({'line': i, 'log': f'{LOG_LINE} - {i}'})

    assert type(lines) is list
    assert len(lines) == 10
    assert lines == expected

    # starting from line 39, reading until line 53 (starting from index 0)
    # should return exactly 15 lines in total
    lines, from_line, to_line = viewer.read(39, 53)
    expected = []
    for i in range(40, 55):
        expected.append({'line': i, 'log': f'{LOG_LINE} - {i}'})

    assert type(lines) is list
    assert len(lines) == 15
    assert lines == expected

    # should return last 2 lines
    lines, from_line, to_line = viewer.read(98, 110)
    expected = []
    for i in range(99, 101):
        expected.append({'line': i, 'log': f'{LOG_LINE} - {i}'})

    assert len(lines) == 2
    assert lines == expected

    delete_log_file()


def test_read_regex():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'read_regex' method is called with $regex parameter
    THEN check that the returned result is lines from file that match the given regular expression
    """

    create_log_file()

    pattern = "- 99"
    viewer = LogViewer(LOG_FILE)
    lines, from_line, to_line = viewer.read_regex(pattern)

    expected = []
    for i in range(99, 100):
        expected.append({'line': i, 'log': f'{LOG_LINE} - {i}'})

    assert type(lines) is list
    assert len(lines) == 1
    assert lines == expected
    assert lines[0]['log'] == expected[0]['log']

    delete_log_file()


def test_read_lines_reverse():
    """
    GIVEN a LogViewer component that reads .log files
    WHEN the 'read_lines_reverse' method is called
    THEN check that the log file is read in reverse, meaning the lines are returned in reverse order starting from
    the last line of the file
    """

    create_log_file()

    with open(LOG_FILE, 'rb') as f:
        gen = LogViewer.read_lines_reverse(f)

        expected = LOG_LINE + ' - 100'
        line = next(gen)
        assert line.decode('utf8').strip() == expected

        expected = LOG_LINE + ' - 99'
        line = next(gen)
        assert line.decode('utf8').strip() == expected

    delete_log_file()
