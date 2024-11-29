from typing import Dict


class Brick(object):

    def __init__(self, label: str, data: Dict[str, str]):
        self.label = label
        self.data = data
        self._sfo_factor = 0  # Score for offer factor
        self._best = False

    def __str__(self):
        return "Brick_name: " + str(self.label) + "Data: " + str(self.data)

    @property
    def sfo_factor(self):
        return self._sfo_factor

    @sfo_factor.setter
    def sfo_factor(self, new_value):
        if 0 <= new_value <= 10:
            self._sfo_factor = new_value

    @property
    def best(self):
        return self.best

    @best.setter
    def best(self, value):
        if value is True or value is False:
            self._best = value
