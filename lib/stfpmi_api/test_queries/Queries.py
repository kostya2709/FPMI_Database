from lib.stfpmi_api.main.StfpmiApi import StfpmiAPI


if __name__ == "__main__":
    info = StfpmiAPI()
    res = info.washing_machine_records("2021-05-07")
    print(res[0])