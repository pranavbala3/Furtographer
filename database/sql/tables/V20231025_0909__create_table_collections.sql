CREATE TABLE collections (
    id           BIGSERIAL       NOT NULL,
    content      VARCHAR(200)    NOT NULL,
    breed        VARCHAR(200)    NOT NULL,
    completed    INTEGER         DEFAULT 0,
    date_created TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    user_id      INTEGER         REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (id)
);
