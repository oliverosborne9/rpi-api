import json
import secrets
from pathlib import Path
from typing import Union

from flask import Flask
from loguru import logger
from mechanic.api.celery.app import start_bg_celery_worker
from mechanic.api.routes.dispense import dispense_blueprint
from mechanic.api.routes.general import general_blueprint
from mechanic.api.routes.scales import scales_blueprint
from mechanic.config.twin import ModuleTwin


def setup_app(config_path: Union[str, Path]) -> Flask:
    """
    Create and configure Flask app, reading config file
    and registering API routes.

    :param config_path: Path to the Module Twin config file
    :return: The configured Flask app
    """
    app = Flask("mechanic")

    app.secret_key = secrets.token_urlsafe(16)

    app.config["TWIN"] = ModuleTwin.from_file(config_path)

    logger.info(f'MODULE TWIN\n{json.dumps(app.config["TWIN"].to_dict(), indent=4)}')

    app.register_blueprint(general_blueprint, url_prefix="/api/v1/")
    app.register_blueprint(scales_blueprint, url_prefix="/api/v1/read")
    app.register_blueprint(dispense_blueprint, url_prefix="/api/v1/dispense")

    return app


def start_app(app: Flask):
    """
    Launch the Flask server, and start a Celery worker
    to handle the asynchronous dispensing tasks.

    :param app: Configured Flask app
    """
    start_bg_celery_worker()
    app.run(host="0.0.0.0", port=7070)  # nosec:B104
