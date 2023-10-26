create table images (
	id      bigserial not null,
	user_id bigserial not null,
	
	primary key (id),
	foreign key (user_id) references users(id)
);

