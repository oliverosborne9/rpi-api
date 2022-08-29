from http import HTTPStatus

from flask import Blueprint, current_app, jsonify
from mechanic.config.twin import ModuleTwin
from mechanic.scales.models import SCALES_MODELS, Scale

scales_blueprint = Blueprint("scales", __name__)


@scales_blueprint.route("/", methods=["GET"])
def all_scales():
    twin: ModuleTwin = current_app.config["TWIN"]
    scale_type = SCALES_MODELS[twin.scales.model]
    response = scale_type(twin.scales.path).get_mass_response()

    if response["status"] == "ok":
        return jsonify(response)
    return jsonify(response), HTTPStatus.NOT_FOUND


@scales_blueprint.route("/<scale>", methods=["GET"])
def single_scales(scale):
    twin: ModuleTwin = current_app.config["TWIN"]
    scale_type: Scale = SCALES_MODELS[twin.scales.model]
    response = scale_type.from_name(scale).get_mass_response()

    if response["status"] == "ok":
        return jsonify(response)
    return jsonify(response), HTTPStatus.NOT_FOUND
