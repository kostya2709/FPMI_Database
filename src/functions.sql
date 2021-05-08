-- Use the tables, belonging to the project
set search_path = 'project';


-- This function allows to list all the students,
-- who live in the room with this room number
drop function if exists room_inhabitants(room_no integer);
create function room_inhabitants(required_room_no integer)
returns table(id integer, name char(20), surname char(20)) as
$$
    begin

    return query
    select student_id, name_txt, surname_txt
    from student
    inner join room r on r.room_id = student.room_id
    where r.room_num = required_room_no;

    end;
$$
language plpgsql;

-- This procedure changes the number of the room from one to another.
-- It is useful if a room needs repair and students
-- have to move to another room
drop procedure if exists resettle(from_ integer, to_ integer);
create procedure resettle(from_ integer, to_ integer)
as
$$
    begin
        update room
        set room_num = to_
        where room_num = from_;
    end;
$$
language plpgsql;

------------------------------------ TESTS ------------------------------------

---------------------------- ROOM INHABITANTS TESTS ---------------------------

-- Get all the inhabitants of the room 201
select *
from room_inhabitants(201);

-- Try to find people from the room, which
-- does not exist. An empty table is expected
select *
from room_inhabitants(2021);

-------------------------------- RESETTLE TESTS -------------------------------

-- Resettle students from one room to another
call resettle(201, 205);
select * from room;

-- Resettle students from a room which
-- does not exist, no changes are expected
call resettle(2021, 205);
select * from room;

-- Resettle students to a room which
-- does not exist, standard behaviour is expected
call resettle(205, 2021);
select * from room;
