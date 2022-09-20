from abc import ABC, abstractmethod
from datetime import datetime


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
