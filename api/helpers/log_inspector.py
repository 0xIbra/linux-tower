from hashlib import md5
import os
import re


class LogInspector:

    def __init__(self, logfile_path):
        self.__logfile_path = logfile_path
        if not os.path.isfile(logfile_path):
            raise Exception(f'{logfile_path} file was not found.')

    def get_first_line_checksum(self):
        first_line = None
        with open(self.__logfile_path) as f:
            for line in f:
                l = line.strip()
                if l != '':
                    first_line = l
                    break

        if first_line is not None:
            first_line = md5(first_line.encode('utf8')).hexdigest()

        return first_line

    def search_regex(self, regex=None, start_line=None):
        detections = []
        line_count = 0
        last_line = None
        with open(self.__logfile_path) as f:
            for i, line in enumerate(f):
                line_count += 1
                last_line = i

                if start_line is not None and i < start_line:
                    continue

                line = line.strip()
                if line == '':
                    continue

                if regex is not None:
                    pattern = re.compile(rf"{regex}")
                    if bool(pattern.search(line)) is True:
                        if len(detections) >= 10:
                            break

                        detections.append({'line': i, 'log': line})

        return line_count, last_line, detections
