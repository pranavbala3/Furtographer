create table users (
	id         bigserial    not null,
	user_name  text         not null,
	first_name text         not null,
	last_name  text         not null,
	pwd        text         not null,
	primary key (id)
);

create unique index uidx_users_user_name on users (user_name);
