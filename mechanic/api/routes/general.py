from http import HTTPStatus

from flask import Blueprint, current_app, jsonify
from mechanic.config.twin import ModuleTwin
from mechanic.scales.models import SCALES_MODELS

general_blueprint = Blueprint("general", __name__)


@general_blueprint.route("/health", methods=["GET"])
def health():
    return "healthy"


@general_blueprint.route("/ready", methods=["GET"])
def ready():

    twin: ModuleTwin = current_app.config["TWIN"]
    scale_type = SCALES_MODELS[twin.scales.model]
    scales = scale_type(twin.scales.path)

    # Check scales are available
    if scales.get_status() == "unavailable":
        return f"{scales.name} UNAVAILABLE", HTTPStatus.NOT_FOUND
    return "ready"


@general_blueprint.route("/twin", methods=["GET"])
def twin():
    """
    The twin endpoint, allowing you to view the current twin
    to check how the app is configured.
    """
    current_twin = current_app.config["TWIN"].to_dict()
    return jsonify(current_twin)
