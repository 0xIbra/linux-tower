from exceptions import ProcessNotFound
import psutil


class Process:

    def __init__(self, name):
        self.__name = name
        self.__pid = None
        self.__process = None

        self.__initialize_process()

    def __initialize_process(self):
        """
        Initializes the process, if no process found running, exception is raised.
        """

        for p in psutil.process_iter():
            if p.name() != self.__name:
                continue

            if self.__pid is None:
                self.__pid = p.pid
            else:
                if p.pid < self.__pid:
                    self.__pid = p.pid

        if self.__pid is None:
            raise ProcessNotFound(f'no process named "{self.__name}" was found running.')

        self.__process = psutil.Process(pid=self.__pid)

    def get_cpu_utilization(self):
        """
        Returns the CPU utilization percentage (all cores).
        """

        cpu_percentages = []
        cpu_utilization = 0
        print(self.__process.children())
        children = self.__process.children()
        if len(children) > 0:
            for child_process in children:
                cpu_percentages.append(child_process.cpu_percent(interval=0.5))
        else:
            cpu_percentages.append(self.__process.cpu_percent(interval=0.5))

        if len(cpu_percentages) > 0:
            cpu_utilization = sum(cpu_percentages) / psutil.cpu_count()

        return cpu_utilization

    def get_memory_usage(self):
        """
        Returns the total of memory used by a program that is running (all cores).
        """

        memory_used = 0
        children = self.__process.children()
        if len(children) > 0:
            for child_process in self.__process.children():
                memory_used += child_process.memory_info().rss
        else:
            memory_used += self.__process.memory_info().rss

        if memory_used > 0:
            memory_used = memory_used / 1024 / 1024

        return memory_used
