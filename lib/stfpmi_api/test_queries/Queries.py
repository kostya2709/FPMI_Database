from lib.stfpmi_api.main.StfpmiApi import StfpmiAPI


def test_washing_machine():
    info_ = StfpmiAPI()
    res_ = info_.washing_machine_records("2021-05-07")
    for i_ in res_:
        print(i_)


def test_scheduled_room_records():
    info_ = StfpmiAPI()
    res_ = res = info_.scheduled_room_record("Переговорная", "2021-05-08")
    for i_ in res_:
        print(i_)

def test_find_person():
    info_ = StfpmiAPI()
    res_ = info_.find_person("Меркурьева")
    print(res_)


if __name__ == "__main__":
    test_scheduled_room_records()
    # test_find_person()