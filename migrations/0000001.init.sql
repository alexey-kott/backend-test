create table authors (
    id bigserial primary key,
    name text not null
);
create table books (
    id bigserial primary key,
    title text not null,
    author_id bigint not null references authors(id) on delete cascade
);
create index books_author_id_idx on books (author_id);

-- Не знаю насколько это можно считать багом и было ли это задумано, но
-- для строковых литералов в PG используются одинарные кавычки. Двойные же нужны для идентификаторов БД.
insert into authors (name) values
    ('Oscar Wilde'), ('Agatha Christie'), ('Mark Twain')
;
insert into books (title, author_id) values
    ('The Picture of Dorian Gray', 1), ('An Ideal Husband', 1), ('Poetry', 1),
    ('The Man in the Brown Suit', 2), ('The Mysterious Affair at Styles', 2),
    ('The Adventures of Tom Sawyer', 3), ('The Adventures of Huckleberry Finn', 3)
;

-- Не очень понятно зачем тут нужна была операция в конце. Тоже "баг"?