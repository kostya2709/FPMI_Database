
set search_path = 'project';


-- function that makes mask over the input string
-- Default behaviour: some_string -> sXXXXXXXXXX
drop function if exists make_mask(str_txt char(27), left_no int, sym_num int, sym_ch character);
create function make_mask(str_txt char(27), left_bound int default 2, sym_num int default -1, sym_ch character default 'X') returns char(27) as
$$
    declare
    x_res char(27) = '';
    input_len int;

    right_bound int;

    begin

    input_len = char_length(str_txt);

    -- Fill the line until the end
    if sym_num = -1
    then
        sym_num = input_len - left_bound + 1;
    end if;

    -- Find the right bound
    right_bound = left_bound + sym_num - 1;


    if sym_num < 0 and sym_num != -1
    then
        raise exception 'Exception in function make_mask. Sym_num should be less then zero!';
    end if;

    if  right_bound > input_len or left_bound < 0
    then
        raise exception 'Exception in function make_mask. Index is out of range!';
    end if;

        x_res = repeat(sym_ch, sym_num);

        str_txt = overlay(str_txt placing x_res from left_bound for sym_num);
        return str_txt;
    end;
$$
language plpgsql;
----------------------------------------------------------------------------------------------------------


-- make_mask() overload for integer input
drop function if exists make_mask(num_no int, left_bound int, sym_num int, sym_ch char(1));
create function make_mask(num_no int, left_bound int default 2, sym_num int default -1, sym_ch char(1) default 'X') returns char(27) as
$$
    begin
        return make_mask(cast(num_no as char(27)), left_bound, sym_num, sym_ch);
    end;
$$
language plpgsql;
----------------------------------------------------------------------------------------------------------

select make_mask(27092001, 2, 4);
select make_mask(cast(27092001 as char(10)), 2, -1, '-');


select * from student;

-- List all PMI students, hiding surname
drop view if exists PMI_students;
create view PMI_students as
select name_txt, make_mask(surname_txt, 2, -1, '*'), group_no
from student
where group_no >= 920 and group_no < 930;

select * from PMI_students;
----------------------------------------------------------------------------------------------------------

-- Count number of PMI students in each room on the second floor,
-- hiding their surnames and the room number, leaving only floor,
-- count people in one room
drop view if exists rooms_PMI;
create view rooms_PMI as
select name_txt,
       make_mask(surname_txt, 4, sym_ch := '*') as surname,
       make_mask(room_num) as room_num,
       count(*) over(partition by room_num order by name_txt) as people_in_room

from student
inner join room
on student.room_id = room.room_id
where group_no >= 920 and group_no < 930
order by room.room_num;

select * from rooms_PMI;
----------------------------------------------------------------------------------------------------------

-- List students and number of students in each group,
-- hide surname, leave the year digit
drop view if exists students_in_groups;
create view students_in_groups as
select name_txt,
       make_mask(surname_txt, 4, sym_ch := '*') as surname,
       make_mask(group_no, 1, 1, '-') as group_no,
       count(*) over (partition by group_no) as num_of_students_in_the_group
from student;

select * from students_in_groups;
----------------------------------------------------------------------------------------------------------

-- Info for dean's office:

-- PMI students:
drop view if exists PMI_students_dean;
create view PMI_students_dean as
select name_txt,
       make_mask(surname_txt, 4, sym_ch := '*') as surname,
       vk_url,
       birth_dt,
       make_mask(room_num) as room_num,
       count(*) over(partition by room_num order by name_txt) as people_in_room

from student
inner join room
on student.room_id = room.room_id
where group_no >= 920 and group_no < 930
order by room.room_num;

select * from PMI_students_dean;
----------------------------------------------------------------------------------------------------------

-- IVT students:
drop view if exists IVT_students_dean;
create view IVT_students_dean as
select name_txt,
       make_mask(surname_txt, 4, sym_ch := '*') as surname,
       vk_url,
       birth_dt,
       make_mask(room_num) as room_num,
       count(*) over(partition by room_num order by name_txt) as people_in_room

from student
inner join room
on student.room_id = room.room_id
where group_no >= 930 and group_no < 940
order by room.room_num;

select * from IVT_students_dean;
----------------------------------------------------------------------------------------------------------

-- KT students:
drop view if exists KT_students_dean;
create view KT_students_dean as
select name_txt,
       make_mask(surname_txt, 4, sym_ch := '*') as surname,
       vk_url,
       birth_dt,
       make_mask(room_num) as room_num,
       count(*) over(partition by room_num order by name_txt) as people_in_room

from student
inner join room
on student.room_id = room.room_id
where group_no >= 910 and group_no < 920
order by room.room_num;

select * from KT_students_dean;
