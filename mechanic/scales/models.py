import time
from datetime import datetime
from random import randrange

from mechanic.scales.base import Scale


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
