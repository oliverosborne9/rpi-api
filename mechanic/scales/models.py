import time
from abc import ABC, abstractmethod
from datetime import datetime
from random import randrange


class Scale(ABC):
    def __init__(self, path: str):
        self.path = path
        self.name = path.split("/")[-1]

    @abstractmethod
    def get_grams(self):
        pass

    @abstractmethod
    def get_weight_tuple(self):
        pass

    def get_status(self):
        return "ok" if self.get_grams() is not None else "unavailable"

    def get_mass_response(self):
        return {
            "mass": self.get_grams(),
            "time": str(datetime.utcnow()),
            "name": self.name,
            "status": self.get_status(),
        }

    @classmethod
    def from_name(cls, name: str) -> "Scale":
        return cls(f"/dev/{name}")


class FakeScale(Scale):
    def get_grams(self):
        time.sleep(0.2)
        return randrange(-10, 500)  # nosec:B311

    def get_weight_tuple(self):
        return (
            self.get_grams(),
            "grams",
            datetime.utcnow(),
            self.path,
            True if randrange(5) != 1 else False,  # nosec:B311
        )


# An implementation for a particular brand of electronic scale,
# using the Human interface device (HID) API,
# has been authored by @drew65 but is omitted from this project
# because the code is intellectual property owned by Recycleye.

SCALES_MODELS = {"FAKE": FakeScale}
