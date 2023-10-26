create table dog_breeds (
	id   bigserial not null,
	images_id  bigserial not null,
	breed_name  text not null,
	
	primary key (id),
	foreign key (images_id) references images
);	