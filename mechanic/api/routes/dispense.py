from dataclasses import asdict
from http import HTTPStatus

from flask import Blueprint, current_app, jsonify, request
from mechanic.api.celery.tasks import dispense
from mechanic.config.twin import ModuleTwin
from mechanic.dispense.methods import DispenseTaskConfig
from mechanic.scales.models import SCALES_MODELS

dispense_blueprint = Blueprint("dispense", __name__)


@dispense_blueprint.route("/async", methods=["POST"])
def dispense_async():
    try:
        colour = request.json["colour"]
        grams = int(request.json["grams"])
    except KeyError as e:
        return f"Field missing from JSON request body: {str(e)}", HTTPStatus.BAD_REQUEST
    except ValueError:
        return "Grams must be given as number", HTTPStatus.BAD_REQUEST

    twin: ModuleTwin = current_app.config["TWIN"]

    try:
        dispenser_config = asdict(twin.containers)[colour]
    except KeyError as e:
        return (
            f"Invalid dispenser colour (must be blue, green, or red): {str(e)}",
            HTTPStatus.BAD_REQUEST,
        )

    scale_type = SCALES_MODELS[twin.scales.model]
    scales = scale_type(twin.scales.path)

    # check scales are available
    return_tuple = f"{scales.name} UNAVAILABLE", HTTPStatus.FAILED_DEPENDENCY
    try:
        if scales.get_status() == "unavailable":
            return return_tuple
    except Exception:
        return return_tuple

    config = DispenseTaskConfig(
        scales_path=twin.scales.path,
        scales_type=twin.scales.model,
        pin=dispenser_config["signalPin"],
        dispense_grams=grams,
    )

    dispense_task = dispense.delay(
        dispense_type=twin.dispensing.method, config=config.to_dict()
    )
    return jsonify({"task_id": dispense_task.id}), HTTPStatus.ACCEPTED


@dispense_blueprint.route("/status/<task_id>")
def taskstatus(task_id):

    task = dispense.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {"state": task.state, "current": 0, "total": 1, "status": "Pending"}
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0) if task.info else 1,
            "total": task.info.get("total", 1) if task.info else 1,
            "status": task.info.get("status", "") if task.info else 1,
        }
        if task.info and "result" in task.info:
            response["result"] = task.info["result"] if task.info else 1
    else:
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),
        }
    return jsonify(response)
