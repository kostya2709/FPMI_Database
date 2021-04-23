from lib.stfpmi_api.main.StfpmiApi import StfpmiAPI


if __name__ == "__main__":
    info = StfpmiAPI()
    res = info.FindPerson("Меркурьева")
    print(res)