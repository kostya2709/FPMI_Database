from lib.stfpmi_api.abstract_class.AbstractInfoClass import AbstractInfoClass


class PersonInfo(AbstractInfoClass):
    '''Full information of a certain person.

    Attributes:
        username: name, used to authorize on the web-site.
        first_name: first_name.
        last_name: surname.
        middle_name: patronymic or father-name.
        img: reference to the image used on the site.
        img_compressed: reference to the compressed image used on the site.
        dormitory: dormitory number(e.g. 2 or 7).
        room_number: room number in the dormitory.
        group_number: group number(e.g. 'Б05-932').
        student_status: current program(e.g. BACHELOR or MAGISTER).
        course_number: number of course.
        phystech_school_name: school name(e.g. 'ФПМИ' or 'ФАКИ').
        birthday:
        email:
        vk_username:
        vk_href:
        telegram_username:
        instagram_username:
        phone_number:
        date_joined:
        activist_info:
    '''

    available_attr = ["username", "first_name", "last_name", "middle_name", "img",
                    "img_compressed", "dormitory", "room_number", "group_number",
                    "student_status", "course_number", "phystech_school_name",
                    "birthday", "email", "vk_username", "vk_href", "telegram_username",
                    "instagram_username", "phone_number", "date_joined", "activist_info"]

    def __init__(self, initial_values: dict):
        PersonInfo.initialize(initial_values, self)