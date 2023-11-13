CREATE TABLE users (
    id         BIGSERIAL       PRIMARY KEY,
    user_name  TEXT         NOT NULL UNIQUE,
    pwd        TEXT         NOT NULL
);

create unique index uidx_users_user_name on users (user_name);
