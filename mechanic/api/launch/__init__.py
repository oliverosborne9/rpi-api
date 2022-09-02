import json
import secrets

from flask import Flask
from loguru import logger
from mechanic.api.celery.app import start_bg_celery_worker
from mechanic.api.routes.dispense import dispense_blueprint
from mechanic.api.routes.general import general_blueprint
from mechanic.api.routes.scales import scales_blueprint
from mechanic.config.twin import ModuleTwin


def start_app():
    app = Flask("mechanic")

    start_bg_celery_worker()

    app.secret_key = secrets.token_urlsafe(16)

    app.config["TWIN"] = ModuleTwin.from_local()

    logger.info(f'MODULE TWIN\n{json.dumps(app.config["TWIN"].to_dict(), indent=4)}')

    app.register_blueprint(general_blueprint, url_prefix="/api/v1/")
    app.register_blueprint(scales_blueprint, url_prefix="/api/v1/read")
    app.register_blueprint(dispense_blueprint, url_prefix="/api/v1/dispense")

    app.run(host="0.0.0.0", port=7070)  # nosec:B104
