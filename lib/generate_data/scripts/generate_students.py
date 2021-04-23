	
import random

def generate_students(room_num):

    male_name_list = ["Константин", "Алексей", "Александр", "Кирилл", "Андрей", "Михаил"]
    female_name_list = ["Эвелина", "Анастасия", "Елизавета", "Светлана", "Екатерина"]
    surname_list = ["Драгун", "Логвиненко", "Беляев", "Русин", "Чуркин", "Саранчин"]

    female_probability = 0.3

    room_mates = 4

    insert_str = "insert into student (name_txt, surname_txt, room_id, group_no) values ('{name}', '{surname}', {room_id}, {group_no}) ON CONFLICT DO NOTHING;"
    file = open("generated_students", "w")

    for i in range(room_num):

        sex = random.uniform(0, 1)

        for j in range(room_mates):

            if sex < female_probability:
                name = random.choice(female_name_list)
            else:
                name = random.choice(male_name_list)

                surname = random.choice(surname_list)
                insert = insert_str.format(name = name, surname = surname, room_id = i + 1, group_no = 900 + random.randint(11, 27))
                file.write(insert)
                file.write("\n")

    file.close()



def generate_rooms(room_num):

    insert_str = "insert into room (dormitory_num, room_num) values ({dormitory}, {room_num});"
    second_dorm_prob = 0.7
    file = open("generated_rooms", "w")

    for i in range(room_num):
        if random.uniform(0, 1) < second_dorm_prob:
            dormitory = 2
        else:
            dormitory = 12
        
        room_num = ((i + 1) % 20) + 200 * ((i // 20) + 1)

        insert = insert_str.format(dormitory = dormitory, room_num = room_num)
        file.write(insert)
        file.write("\n")
    
    file.close()
        

        

if __name__ == "__main__":

    room_num = 15
    generate_students(room_num)
    generate_rooms(room_num)