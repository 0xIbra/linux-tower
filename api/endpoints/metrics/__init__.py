from endpoints import blueprint
from entities import CpuMetric, MemoryMetric, DiskMetric
from flask import jsonify, request
from api import db
from decorators import is_authenticated
from datetime import datetime, timedelta


def parse_since_param(since_param):
    if since_param is not None:
        since = datetime.strptime(since_param, '%Y-%m-%d')
    else:
        since = datetime.now() - timedelta(hours=24)

    return since


@blueprint.route('/api/metrics/cpu', methods=['GET'])
@is_authenticated
def get_cpu_metric_data():
    since = parse_since_param(request.args.get('since'))
    program = request.args.get('program')
    metrics = db.session.query(CpuMetric).filter((CpuMetric.created_at >= since) & (CpuMetric.program == program)).all()

    return jsonify([x.to_json() for x in metrics])


@blueprint.route('/api/metrics/memory', methods=['GET'])
@is_authenticated
def get_memory_metric_data():
    since = parse_since_param(request.args.get('since'))
    program = request.args.get('program')
    metrics = db.session.query(MemoryMetric).filter((MemoryMetric.created_at >= since) & (MemoryMetric.program == program)).all()

    return jsonify([x.to_json() for x in metrics])


@blueprint.route('/api/metrics/disk', methods=['GET'])
@is_authenticated
def get_disk_metric_data():
    since = parse_since_param(request.args.get('since'))
    metrics = db.session.query(DiskMetric).filter(DiskMetric.created_at >= since).all()

    return jsonify([x.to_json() for x in metrics])
