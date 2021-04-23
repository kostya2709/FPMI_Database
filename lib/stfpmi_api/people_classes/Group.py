from lib.stfpmi_api.abstract_class.AbstractInfoClass import AbstractInfoClass
from lib.stfpmi_api.people_classes.PersonInfo import PersonInfo


class GroupInfo:
    def __init__(self, group: dict):

        if len(group) > 2:
            raise RuntimeError("Invalid attributes in GroupInfo.")

        for key, value in group.items():                    # Only one iteration is expected
            self.group_no = key
            self.people = list(map(PersonInfo, value))