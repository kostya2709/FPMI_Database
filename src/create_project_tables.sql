set search_path = 'project';

drop schema if exists project cascade;
create schema project;

---------------------------- STUDENT -----------------------------

drop table if exists student cascade;
create table student (
    student_id serial,
    name_txt char(20) NOT NULL,
    surname_txt char(20) NOT NULL,
    patronymic_txt char(20),
    room_id integer,
    phystech_school_cd char(3),
    group_no integer,
    birth_dt date,
    email_url char(40),
    vk_url char(40),
    telegram_url char(40),
    valid_from_dttm timestamp (0),
    valid_to_dttm timestamp (0),

    constraint pk_student primary key (student_id)
);

----------------------------- ROOM ------------------------------

drop table if exists room cascade;
create table room (
  room_id serial primary key,
  dormitory_num integer,
  room_num integer NOT NULL
);

alter table student add constraint FKToRoom
foreign key (room_id) references room(room_id);


---------------------------- FURNITURE ----------------------------

drop table if exists furniture cascade;
create table furniture (
  furniture_id bigint primary key,
  room_id integer NOT NULL,
  furniture_type_txt char(50),
  constraint FK_To_Furniture
  foreign key (room_id) references room(room_id)
);



------------------------- RESERVATION TABLE---------------------------

drop table if exists reservation_table cascade;
create table reservation_table (
  reservation_id serial primary key,
  special_room_id integer,
  student_id int NOT NULL,
  time_start_dttm timestamp,
  time_finish_dttm timestamp
);



----------------------- SPECIAL ROOM --------------------------------

drop table if exists special_room cascade;
create table special_room (
  special_room_id serial primary key,
  dormitory_num integer,
  full_room_nm char(40) NOT NULL,
  short_room_nm char(20),
  floor_num smallint,
  eat_permission_flg bool
);

alter table reservation_table add constraint FK_To_Special_Room
foreign key (special_room_id) references special_room(special_room_id);



------------------ STUDENT_X_RESERVATION_TABLE ------------------------

create table student_x_reservation_table (
    student_id integer NOT NULL,
    reservation_id integer NOT NULL,

    constraint FK_To_Student
    foreign key (student_id) references student(student_id),

    constraint FK_To_Reserve
    foreign key (reservation_id) references reservation_table(reservation_id)
);