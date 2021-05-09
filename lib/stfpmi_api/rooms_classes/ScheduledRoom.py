from lib.stfpmi_api.abstract_class.AbstractInfoClass import AbstractInfoClass
from lib.stfpmi_api.people_classes.ShortPersonInfo import ShortPersonInfo


class ScheduledRoom(AbstractInfoClass):
    available_attr = ["id", "scheduled_room_component", "title", "initiator",
                      "participants", "open_for_everyone", "approved", "start_time", "end_time"]

    def __init__(self, initial_values: dict):
        ScheduledRoom.initialize(initial_values, self)
        self.initiator = ShortPersonInfo(self.initiator)
        self.participants = list(map(ShortPersonInfo, self.participants))


if __name__ == "__main__":
    pass