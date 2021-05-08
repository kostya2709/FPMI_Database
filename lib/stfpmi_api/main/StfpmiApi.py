from lib.stfpmi_api.people_classes.PersonInfo import PersonInfo
from lib.stfpmi_api.people_classes.ShortPersonInfo import ShortPersonInfo
from lib.stfpmi_api.people_classes.Group import GroupInfo
from datetime import datetime
import requests

class SpecialRoom:
    washing = 2

class StfpmiAPI:
    def __init__(self):
        self.__token = self.__GetToken()
        self.__headers = {"accept": "application/json", "Authorization": self.__token}

    def __GetToken(self):
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
            token = self.__Authorize()
            with open(token_file_name, 'w') as token_file:
                token_file.write(token)

        except:
            raise RuntimeError("An unexpected exception while getting a token!")

        return token

    def __Authorize(self):
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