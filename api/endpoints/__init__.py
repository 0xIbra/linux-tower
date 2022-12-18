from flask import Blueprint

blueprint = Blueprint('api_blueprint', __name__)

from endpoints import system_metrics, processes, apache, nginx, log_reader
from endpoints.alerts import *
from endpoints.auth import *
