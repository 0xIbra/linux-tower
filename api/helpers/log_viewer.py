import os


class LogViewer:

    def __init__(self, log_file):
        self.__log_file = log_file
        if not os.path.isfile(log_file):
            raise Exception(f'{log_file} file was not found.')

    def head(self, lines=10):
        with open(self.__log_file) as file:
            logs = []
            line = next(file)
            for x in range(lines):
                logs.append(line.strip())

                try:
                    line = next(file)
                except:
                    line = None

        return logs

    def tail(self, lines=10):
        f = open(self.__log_file, 'rb')
        total_lines_wanted = lines

        BLOCK_SIZE = 1024
        f.seek(0, 2)
        block_end_byte = f.tell()
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = []
        while lines_to_go > 0 and block_end_byte > 0:
            if (block_end_byte - BLOCK_SIZE > 0):
                f.seek(block_number * BLOCK_SIZE, 2)
                blocks.append(f.read(BLOCK_SIZE))
            else:
                f.seek(0, 0)
                blocks.append(f.read(block_end_byte))
            lines_found = blocks[-1].count(b'\n')
            lines_to_go -= lines_found
            block_end_byte -= BLOCK_SIZE
            block_number -= 1

        all_read_text = b''.join(reversed(blocks))
        f.close()
        byte_logs = all_read_text.splitlines()[-total_lines_wanted:]
        logs = []
        for l in byte_logs:
            logs.append(l.decode('utf8'))

        return logs

    def readall(self):
        with open(self.__log_file) as f:
            logs = f.read().splitlines()

        return logs

    def read(self, from_line, to_line):
        logs = []
        fp = open(self.__log_file)
        for i, line in enumerate(fp):
            if from_line <= i <= to_line:
                logs.append(line.strip())
        fp.close()

        return logs

    @staticmethod
    def read_lines_reverse(f):
        head = b""
        f.seek(0, 2)
        t = f.tell()
        buffersize, maxbuffersize = 64, 4096
        while True:
            if t <= 0:
                break
            # Read next block
            buffersize = min(buffersize * 2, maxbuffersize)
            tprev = t
            t = max(0, t - buffersize)
            f.seek(t)
            lines = f.read(tprev - t).splitlines(True)
            # Align to line breaks
            if not lines[-1].endswith((b"\n", b"\r")):
                lines[-1] += head  # current tail is previous head
            elif head == b"\n" and lines[-1].endswith(b"\r"):
                lines[-1] += head  # Keep \r\n together
            elif head:
                lines.append(head)
            head = lines.pop(0)  # can be '\n' (ok)
            # Iterate over current block in reverse
            for line in reversed(lines):
                yield line
        if head:
            yield head
