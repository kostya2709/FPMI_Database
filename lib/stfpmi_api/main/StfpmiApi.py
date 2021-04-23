from lib.stfpmi_api.people_classes.PersonInfo import PersonInfo
from lib.stfpmi_api.people_classes.ShortPersonInfo import ShortPersonInfo
from lib.stfpmi_api.people_classes.Group import GroupInfo
from datetime import datetime
import requests

class SpecialRoom:
    washing = 2

class StfpmiAPI:
    def __init__(self):
        with open('main/token') as token_file:
            self.__token = token_file.read()
        self.__headers = {"accept": "application/json", "Authorization": self.__token}

    def FindPerson(self, surname):
        username = str(surname.encode("utf-8"))[2: -1]  # Skip initial and final symbols: b'some_string' -> some_string
        username = username.replace("\\x",
                                    "%").upper()  # Prepare the string: \xd0\x94\xd1\x80\xd0\xb0\xd0\xb3\xd1\x83\xd0\xbd ->
        #                   -> %D0%94%D1%80%D0%B0%D0%B3%D1%83%D0%BD

        url = f"https://stfpmi.ru/api/accounts/search/{username}"
        response = requests.get(url, headers=self.__headers)
        return PersonInfo(response.json()[0])

    def GetUserInfo(self):
        url = "https://stfpmi.ru/api/accounts/profile/my"
        response = requests.get(url, headers=self.__headers)
        return PersonInfo(response.json())

    def FindGroupInfo(self, group_no):
        url = "https://stfpmi.ru/api/accounts/search_by_groupname/" + str(group_no)
        response = requests.get(url, headers=self.__headers)
        return GroupInfo(response.json())

    def WashingMachine(self, begin_time_iso, end_time_iso=datetime.now().isoformat()):
        url = f"https://stfpmi.ru/api/washing/all_records/{SpecialRoom.washing}/{begin_time_iso}/{end_time_iso}"
        response = requests.get(url, headers=self.__headers)
        return list(map(WashingMachine, response.json()))