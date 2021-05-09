from lib.stfpmi_api.people_classes.PersonInfo import PersonInfo
from lib.stfpmi_api.people_classes.ShortPersonInfo import ShortPersonInfo
from lib.stfpmi_api.people_classes.Group import GroupInfo

from lib.stfpmi_api.rooms_classes.WashingMachine import WashingMachine
from lib.stfpmi_api.rooms_classes.ScheduledRoom import ScheduledRoom

from datetime import datetime
import requests


class SpecialRoom:
    washing = 2
    room_id = {"клуб": 1,
               "игровая": 2,
               "кдс": 3,
               "комната для собраний": 3,
               "переговорная": 4}

class StfpmiAPI:
    def __init__(self):
        self.__token = self._get_token()
        self.__headers = {"accept": "application/json", "Authorization": self.__token}

    def _get_token(self):
        """This method gives an available token. If the user is already authorized,
        the token is stored in file "main/token". Otherwise the method requests
        user's username and password.

        Exception:
            RuntimeError:   something went wrong while getting token.

        """
        token = ""
        token_file_name = "main/token"

        # If the user is already authorized, token is stored in the special file.
        try:
            with open(token_file_name, "r") as token_file:
                token = token_file.read()

        # If the file does not exist, the user is not authorized. Let's authorize and save
        # the token into the file.
        except FileNotFoundError as error:
            token = self._authorize()
            with open(token_file_name, 'w') as token_file:
                token_file.write(token)

        except:
            raise RuntimeError("An unexpected exception while getting a token!")

        return token

    def _authorize(self):
        url = f"https://stfpmi.ru/api/login"
        print("You have not been authorized yet.")
        username = input("Insert your username: ")
        password = input("Insert your password: ")
        response = requests.post(url, data={"username": username, "password": password})

        if response.status_code == 200:
            print("You have been successfully authorized!\n")
        else:
            raise RuntimeError("An error occurred while trying to authorize.")

        return response.json()["token"]

    def find_person(self, surname):
        """Find a person by his surname."""

        username = str(surname.encode("utf-8"))[2: -1]  # Skip initial and final symbols: b'some_string' -> some_string
        username = username.replace("\\x",
                                    "%").upper()    # Prepare the string: \xd0\x94\xd1\x80\xd0\xb0\xd0\xb3\xd1\x83\xd0\xbd ->
                                                    #                   -> %D0%94%D1%80%D0%B0%D0%B3%D1%83%D0%BD

        url = f"https://stfpmi.ru/api/accounts/search/{username}"
        response = requests.get(url, headers=self.__headers)
        return self.find_person_by_user_name(response.json()[0]["username"])

    def find_person_by_user_name(self, username):
        """"Find person by username on the web-site."""

        url = f"https://stfpmi.ru/api/accounts/profile/{username}"
        response = requests.get(url, headers=self.__headers)
        return PersonInfo(response.json())

    def get_user_info(self):
        url = "https://stfpmi.ru/api/accounts/profile/my"
        response = requests.get(url, headers=self.__headers)
        return PersonInfo(response.json())

    def find_group_info(self, group_no):
        url = "https://stfpmi.ru/api/accounts/search_by_groupname/" + str(group_no)
        response = requests.get(url, headers=self.__headers)
        return GroupInfo(response.json())

    def washing_machine_records(self, begin_time_iso, end_time_iso=datetime.now().isoformat()):
        url = f"https://stfpmi.ru/api/washing/all_records/{SpecialRoom.washing}/{begin_time_iso}/{end_time_iso}"
        response = requests.get(url, headers=self.__headers)
        return list(map(WashingMachine, response.json()))

    def scheduled_room_record(self, room_name, begin_time_iso, end_time_iso=datetime.now().isoformat()):
        """Give information about records in a scheduled room.

        Arguments:
            room_name:          name of a scheduled room (e.g. "клуб") in both lowercase and uppercase.
            begin_time_iso:     time of the event start.
            end_time_iso:       time of the event end (current time by default).

        Exception:
            RuntimeError:       if the "room_name" does not correspond to any real room name.

        """
        room_name_low = room_name.lower()
        scheduled_room_component_id = SpecialRoom.room_id[room_name_low]

        if scheduled_room_component_id is None:
            raise RuntimeError("Error! Unexpected room " + room_name + "!")

        url = f"https://stfpmi.ru/api/scheduled_rooms/all_records/{scheduled_room_component_id}/{begin_time_iso}/{end_time_iso}"
        response = requests.get(url, headers=self.__headers)
        return list(map(ScheduledRoom, response.json()))
