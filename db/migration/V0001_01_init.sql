drop table
    if exists
    hyperativa.t_user;

create table
    if not exists
    hyperativa.t_user(
        id bigint not null auto_increment,
        name varchar(255) not null,
        is_active boolean not null default True,
        username varchar(8) not null,
        password varchar(255) not null,
        created_at datetime not null,
        updated_at datetime not null,
        constraint primary key pk_t_user (id),
        constraint unique uc_t_user (name)
);

insert into t_user (id, name, is_active, username, password, created_at, updated_at)
values (null, 'Steve Perry',
        1, 'sperry',
        'gAAAAABmsuqqBy84s5d9MM6ORqXZciKaLXvxEUSEiFPcip8Btl5oWpw5EvPRo_xlKH9_PMQHIY2vrgc9-ws4D3IrTzxDnXzwLg==',
        '2024-08-07 03:31:40',
        '2024-08-07 03:31:40');

drop table
    if exists
    hyperativa.t_header cascade;


create table
    if not exists
    hyperativa.t_header(
        id bigint not null auto_increment,
        name varchar(29) not null,
        date varchar(8) not null,
        batch_name varchar(8) not null,
        registers int not null default 1,
        created_at timestamp not null,
        updated_at timestamp not null,
        constraint primary key pk_t_header (id),
        constraint unique uc_t_header (name)
);

drop table
    if exists
    hyperativa.t_item cascade;


create table
    if not exists
    hyperativa.t_item(
        id bigint not null auto_increment,
        header_id bigint not null,
        line int not null,
        batch_number int not null,
        credit_card_number varchar(255) not null,
        created_at timestamp not null,
        updated_at timestamp not null,
        constraint unique uc_t_item(credit_card_number),
        constraint primary key pk_t_item (id),
        constraint foreign key fk_t_header(header_id) references t_header(id)
);

