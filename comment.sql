drop database if exists comments_database;
create database comments_database;
use comments_database;
drop table if exists comments;
create table comments(
    comment_id bigint auto_increment,
    post_id bigint not null ,
    user_id bigint not null ,
    content text,
    constraint comments_pk primary key (comment_id)
);

alter table comments
modify column comment_id bigint auto_increment;

