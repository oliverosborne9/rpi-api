import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Union

from dataclasses_json import LetterCase, dataclass_json
from mechanic.api.celery.tasks import DISPENSE_METHODS
from mechanic.scales.models import SCALES_MODELS


def validate_choice_against_dict(selection: str, reference_dict: Dict):
    # Check selection can be mapped to required callable
    available_choices = reference_dict.keys()
    if selection not in available_choices:
        raise ValueError(f"Dispense type not in {available_choices}")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class ContainerParams:
    """
    A structure to handle each dispensing container's servo motor.
    Each servo motor has three cables to the GPIO pins on the Raspberry Pi.
    """

    plus_pin: int = 0
    minus_pin: int = 0
    signal_pin: int = 0


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class ContainerConfig:
    """
    Servo motor setup for each of the three dispensing containers,
    named red, green and blue.
    """

    blue: ContainerParams = field(default_factory=ContainerParams)
    green: ContainerParams = field(default_factory=ContainerParams)
    red: ContainerParams = field(default_factory=ContainerParams)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class DispenseMechanics:
    """
    Configuration of the method of dispensing.
    """

    # Default to first key of DISPENSE_METHODS, i.e. "DUMMY"
    method: str = next(iter(DISPENSE_METHODS))

    def __post_init__(self):
        self.method = self.method.upper()

        # Check can be mapped to dispensing function
        validate_choice_against_dict(self.method, DISPENSE_METHODS)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class ScalesConfig:
    path: str = ""
    # Default model to first key of SCALES_MODELS, i.e. "FAKE"
    model: str = next(iter(SCALES_MODELS))

    def __post_init__(self):
        self.model = self.model.upper()

        # Check can be mapped to dispensing function
        validate_choice_against_dict(self.model, SCALES_MODELS)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass()
class ModuleTwin:
    """
    Dataclass containing all configurable options for the module.
    config.template.json indicates JSON schema.

    :param scales_path: Unix path to the electronic weighing scales
        connected to the Raspberry Pi (and binding into the container),
        typically with root directory /dev
    :param containers: The configuration of the servo motor connections
        to each dispensing container
    """

    containers: ContainerConfig = field(default_factory=ContainerConfig)
    dispensing: DispenseMechanics = field(default_factory=DispenseMechanics)
    scales: ScalesConfig = field(default_factory=ScalesConfig)

    @classmethod
    def from_file(cls, json_file_path: Union[str, Path]) -> "ModuleTwin":
        """
        :param json_file: Path to the JSON file containing configuration
        :return: The loaded module twin, used to configure the app
        """
        with open(json_file_path, "r") as file:
            config = json.load(file)
        return cls.from_dict(config)
