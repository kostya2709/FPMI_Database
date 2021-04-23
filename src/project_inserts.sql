set search_path = 'project';

----------------------------- ROOM ------------------------------

insert into room (dormitory_num, room_num) values (2, 233);


---------------------------- STUDENT -----------------------------

insert into student values (1, 'Константин', 'Драгун', 'Юрьевич', 1, 'Б05', 932, '2001-09-27',
                     'k.dragun.k@mail.ru', 'https://vk.com/k.dragun', '@dragun_konstantin', '2021-04-06 17:38', clock_timestamp()) ON CONFLICT DO NOTHING;

insert into student (name_txt, surname_txt) values ('Кирилл', 'Кязимов');


---------------------------- FURNITURE ----------------------------

insert into furniture values (210136117456, 1, 'table');


-------------------------- SPECIAL ROOM ----------------------------

insert into special_room (dormitory_num, full_room_nm, short_room_nm, floor_num, eat_permission_flg)
values (2, 'Комната для собраний', 'КДС', 1, false);

insert into special_room (dormitory_num, full_room_nm, short_room_nm, floor_num, eat_permission_flg)
values (2, 'Игровая комната', 'Игровая', 1, false);

insert into special_room (dormitory_num, full_room_nm, short_room_nm, floor_num, eat_permission_flg)
values (2, 'Переговорная комната', 'Переговорка', 1, false);

insert into special_room (dormitory_num, full_room_nm, short_room_nm, floor_num, eat_permission_flg)
values (2, 'Стиральная комната', 'Стиралка', 2, true);

insert into special_room (dormitory_num, full_room_nm, short_room_nm, floor_num, eat_permission_flg)
values (2, 'Читальный зал', 'Боталка', 1, true);

insert into special_room (dormitory_num, full_room_nm, short_room_nm, floor_num, eat_permission_flg)
values (2, 'Комната с инструментами', 'Инструментарий', 1, true);
