from http import HTTPStatus

from flask import Blueprint, current_app, jsonify
from mechanic.config.twin import ModuleTwin
from mechanic.dispense.methods import DispenseTaskConfig
from mechanic.scales.hid import ScaleReadError
from mechanic.scales.models import SCALES_MODELS

dispense_blueprint = Blueprint("dispense", __name__)


@dispense_blueprint.route("/async", methods=["POST"])
def dispense_async():
    # dispense_r = int(request.data)
    twin: ModuleTwin = current_app.config["TWIN"]
    scale_type = SCALES_MODELS[twin.scales.model]
    scales = scale_type(twin.scales.path)

    # check scales are available
    return_tuple = f"{scales.name} UNAVAILABLE", HTTPStatus.FAILED_DEPENDENCY
    try:
        if scales.get_status() == "unavailable":
            return return_tuple
    except ScaleReadError:
        return return_tuple

    from mechanic.api.celery.tasks import dispense

    config = DispenseTaskConfig(
        scales_path=twin.scales.path, scales_type=twin.scales.model
    )

    dispense_task = dispense.delay(
        dispense_type=twin.dispensing.method, config=config.to_dict()
    )
    return jsonify({"task_id": dispense_task.id}), HTTPStatus.ACCEPTED


@dispense_blueprint.route("/status/<task_id>")
def taskstatus(task_id):
    from mechanic.api.celery.tasks import dispense

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
