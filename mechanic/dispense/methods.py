from dataclasses import dataclass
from time import sleep, time
from typing import Dict

from celery import current_task
from dataclasses_json import LetterCase, dataclass_json
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from mechanic.scales.models import SCALES_MODELS, Scale


@dataclass_json(letter_case=LetterCase.CAMEL)  # necessary for Dict serialisation
@dataclass()
class DispenseTaskConfig:
    scales_path: str
    scales_type: str
    pin: int = 0
    dispense_grams: int = 0
    forward_dur_sec: float = 0.5
    backward_dur_sec: float = 0.2
    servo_value: float = 0.5


# IP address of the gateway between the Docker host
# and the (default) bridge network
HOST_IP = "172.17.0.1"


def get_servo(servo_pin: int, host: str = HOST_IP):
    factory = PiGPIOFactory(host=host)
    return Servo(servo_pin, pin_factory=factory)


def standard_dispense(config: Dict):
    # Celery tasks must have the args sent as JSON serialisable values.
    # After sent they can be converted back to the dataclass.
    config: DispenseTaskConfig = DispenseTaskConfig.from_dict(config)

    # TODO: handle timeout

    scales: Scale = SCALES_MODELS[config.scales_type](path=config.scales_path)
    mass = scales.get_grams()
    target_mass = mass - config.dispense_grams

    servo = get_servo(config.pin)
    servo.value = config.servo_value
    last_change_time = time()

    durs = {True: config.forward_dur_sec, False: config.backward_dur_sec}

    while mass > target_mass:
        current_time = time()
        mass = scales.get_grams()
        dur = durs[servo.value > 0]
        if current_time - last_change_time > dur:
            servo.value *= -1
            last_change_time = current_time
    servo.value = 0


def dummy_dispense(config: Dict):
    total = 20
    for i in range(total):
        sleep(1)
        current_task.update_state(state="PROGRESS", meta={"current": i, "total": total})


DISPENSE_METHODS = {"DUMMY": dummy_dispense, "STANDARD": standard_dispense}
