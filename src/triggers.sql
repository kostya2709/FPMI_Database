-- Use the tables, belonging to the project
set search_path = 'project';

------------------------------ ACCOMMODATION LOGS -----------------------------

-- Create a new table for accommodation logs
drop table if exists resettlement_table_log;
create table resettlement_table_log (
    log_id serial,
    trigger_nm char(27),
    operation_nm char(27),
    table_nm char(27),
    time_dt date,
    old_room_id char(27),
    new_room_id char(27)
);

-- This function is invoked by the triggers when something changes
-- with a person's room_id
drop function if exists resettlement_table_log_function() cascade;
create function resettlement_table_log_function() returns trigger as
$$
    begin
        if (tg_op = 'UPDATE') and (new.room_id <> old.room_id) then
        insert into resettlement_table_log (trigger_nm, operation_nm, table_nm, time_dt, old_room_id, new_room_id)
                        values (tg_name, tg_op, tg_table_name, now(), old.room_id, new.room_id);

        elseif (tg_op = 'DELETE') then
        insert into resettlement_table_log (trigger_nm, operation_nm, table_nm, time_dt, old_room_id, new_room_id)
            values (tg_name, tg_op, tg_table_name, now(), old.room_id, null);

        elseif (tg_op = 'INSERT') then
        insert into resettlement_table_log (trigger_nm, operation_nm, table_nm, time_dt, old_room_id, new_room_id)
            values (tg_name, tg_op, tg_table_name, now(), null, new.room_id);
        end if;

        return new;

    end;
$$
language plpgsql;


-- They are divided because only in update it is
-- possible to compare old and new
drop trigger if exists room_changing on student;
create trigger room_changing
    after update on student
    for each row
    when (old.* is distinct from new.*)
    execute function resettlement_table_log_function();

-- A standard trigger to insert and delete to student table
drop trigger if exists resettlement on student;
create trigger resettlement
    after delete or insert on student
    for each row
    execute function resettlement_table_log_function();


------------------------------ GROUP CHANGING LOGS -----------------------------

-- Create a new table for group changing logs
drop table if exists group_change_table_log;
create table group_change_table_log (
    log_id serial,
    trigger_nm char(27),
    operation_nm char(27),
    table_nm char(27),
    student_id integer,
    time_dt date,
    old_group_no char(27),
    new_group_no char(27)
);

-- This function is invoked by the triggers when something changes
-- with a person's group (enrollment, changing, expulsion)
drop function if exists group_change_table_log_function() cascade;
create function group_change_table_log_function() returns trigger as
$$
    begin
        if (tg_op = 'UPDATE') and (new.group_no <> old.group_no) then
        insert into group_change_table_log (trigger_nm, operation_nm, table_nm, student_id, time_dt, old_group_no, new_group_no)
                        values (tg_name, tg_op, tg_table_name, new.student_id, now(), old.group_no, new.group_no);

        elseif (tg_op = 'DELETE') then
        insert into group_change_table_log (trigger_nm, operation_nm, table_nm, student_id, time_dt, old_group_no, new_group_no)
            values (tg_name, tg_op, tg_table_name, old.student_id, now(), old.group_no, null);

        elseif (tg_op = 'INSERT') then
        insert into group_change_table_log (trigger_nm, operation_nm, table_nm, student_id, time_dt, old_group_no, new_group_no)
            values (tg_name, tg_op, tg_table_name, new.student_id, now(), null, new.group_no);
        end if;

        return new;

    end;
$$
language plpgsql;


-- They are divided because only in update it is
-- possible to compare old and new
drop trigger if exists group_changing on student;
create trigger group_changing
    after update on student
    for each row
    when (old.* is distinct from new.*)
    execute function group_change_table_log_function();

-- A standard trigger to insert to student table
drop trigger if exists student_expulsion on student;
create trigger student_expulsion
    after delete on student
    for each row
    execute function group_change_table_log_function();

-- A standard trigger to delete to student table
-- N.B. There are two triggers for enrollment and expulsion
-- to reflect the action in it's name
drop trigger if exists new_student_enrollment on student;
create trigger new_student_enrollment
    after insert on student
    for each row
    execute function group_change_table_log_function();


------------------------------------ TESTS ------------------------------------

--------------------------- ACCOMMODATION LOGS TESTS --------------------------

-- New line is created in resettlement_table_log as a new inhabitant appeared
insert into student (name_txt, surname_txt, room_id, group_no)
values ('Кирилл', 'Кязимов', 11, 932) ON CONFLICT DO NOTHING;
select * from resettlement_table_log;

-- New line is created in resettlement_table_log as a room id has changed
update student
set room_id = 3
where surname_txt = 'Кязимов';
select * from resettlement_table_log;

-- New line is NOT created in resettlement_table_log as a room id has NOT changed
update student
set email_url = 'new_mail@yandex.ru'
where surname_txt = 'Кязимов';
select * from resettlement_table_log;

-- New line is created in resettlement_table_log as an inhabitant has left the room
delete from student
where surname_txt = 'Кязимов';
select * from resettlement_table_log;


-------------------------- GROUP CHANGING LOGS TESTS --------------------------

-- New line is created in group_change_table_log as a new student has appeared
insert into student (name_txt, surname_txt, room_id, group_no)
values ('Александр', 'Пиперски', 11, 927) ON CONFLICT DO NOTHING;
select * from group_change_table_log;

-- New line is created in group_change_table_log as a group has changed
update student
set group_no = 3
where surname_txt = 'Пиперски';
select * from group_change_table_log;

-- New line is NOT created in group_change_table_log as a group has NOT changed
update student
set telegram_url = '@piprski'
where surname_txt = 'Пиперски';
select * from group_change_table_log;

-- New line is created in group_change_table_log as a student has left the group
delete from student
where surname_txt = 'Пиперски';
select * from group_change_table_log;