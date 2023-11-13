create table collections (
    id   bigserial not null,
    content  varchar(200) not null,
    breed  varchar(200) not null,
    completed  integer default 0,
    date_created  timestamp default current_timestamp,
    
    primary key (id)
);
