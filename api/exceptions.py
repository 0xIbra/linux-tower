class ProcessNotFound(Exception):
    """Raised when a process is not found running on system."""
    pass


class ApacheNotRunning(Exception):
    """Raised when `apache2` service is not running."""
    pass


class NginxNotRunning(Exception):
    """Raised when `nginx` service is not running."""
    pass
