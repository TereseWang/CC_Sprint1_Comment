drop database if exists comments_database;
create database comments_database;
use comments_database;
drop table if exists comments;
create table comments(
    comment_id bigint ,
    post_id bigint not null ,
    user_id bigint not null ,
    content text,
    constraint comments_pk primary key (comment_id)
);

