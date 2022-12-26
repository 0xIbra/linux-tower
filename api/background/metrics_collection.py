from helpers.metrics import system_metrics
from entities import CpuMetric, MemoryMetric, DiskMetric
from helpers.programs import Apache, Nginx, MySQL
from datetime import datetime
from api import db


def metrics_collection(*args):
    """
    Background task, called every x seconds/minutes/hours.
    Collects system usage data and saves to db.
    """

    app = args[0]
    with app.app_context():
        # collect general
        sys_metrics = system_metrics()
        now = datetime.now()

        cpu_metric = CpuMetric(value=sys_metrics['cpu_usage'], created_at=now)
        memory_metric = MemoryMetric(value=sys_metrics['memory']['percent'], created_at=now)
        disk_metric = DiskMetric(value=sys_metrics['disk']['percent'], created_at=now)

        db.session.add(cpu_metric)
        db.session.add(memory_metric)
        db.session.add(disk_metric)

        # web server
        if Apache.is_installed():
            try:
                metrics = Apache.metrics()
                cpu_metric = CpuMetric(value=metrics['cpu_usage'], created_at=now, program=Apache.LABEL)
                memory_metric = MemoryMetric(value=metrics['memory']['percent'], created_at=now, program=Apache.LABEL)
                db.session.add(cpu_metric)
                db.session.add(memory_metric)
            except Exception:
                pass
        elif Nginx.is_installed():
            try:
                metrics = Nginx.metrics()
                cpu_metric = CpuMetric(value=metrics['cpu_usage'], created_at=now, program=Nginx.LABEL)
                memory_metric = MemoryMetric(value=metrics['memory']['percent'], created_at=now, program=Nginx.LABEL)
                db.session.add(cpu_metric)
                db.session.add(memory_metric)
            except Exception:
                pass

        # mysql
        if MySQL.is_installed():
            try:
                metrics = MySQL.metrics()
                cpu_metric = CpuMetric(value=metrics['cpu_usage'], created_at=now, program=MySQL.LABEL)
                memory_metric = MemoryMetric(value=metrics['memory']['percent'], created_at=now, program=MySQL.LABEL)
                db.session.add(cpu_metric)
                db.session.add(memory_metric)
            except Exception:
                pass

        # commit db
        db.session.commit()
