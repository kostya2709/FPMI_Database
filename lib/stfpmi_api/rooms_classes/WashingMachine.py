from lib.stfpmi_api.abstract_class.AbstractInfoClass import AbstractInfoClass
from lib.stfpmi_api.people_classes.ShortPersonInfo import ShortPersonInfo
from datetime import datetime


class WashingMachine(AbstractInfoClass):
    available_attr = ["id", "machine", "user", "start_time", "end_time"]

    def __init__(self, initial_values: dict):
        WashingMachine.initialize(initial_values, self)
        self.user = ShortPersonInfo(self.user)


if __name__ == "__main__":
    pass