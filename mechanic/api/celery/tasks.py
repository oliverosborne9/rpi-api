from typing import Dict

from mechanic.api.celery.app import CELERY_APP
from mechanic.dispense.methods import DISPENSE_METHODS


@CELERY_APP.task
def dispense(dispense_type: str, config: Dict):
    dispense_function = DISPENSE_METHODS[dispense_type]
    dispense_function(config=config)
