from lib.stfpmi_api.abstract_class.AbstractInfoClass import AbstractInfoClass


class ShortPersonInfo(AbstractInfoClass):
    available_attr = ["id", "username", "first_name", "last_name", "img"]

    def __init__(self, initial_values):
        ShortPersonInfo.initialize(initial_values, self)
