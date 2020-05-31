CREATE TABLE user_account (
    id SERIAL PRIMARY KEY,
    name_hashed CHAR(128) UNIQUE NOT NULL,
    name_encrypted VARCHAR(128) NOT NULL,
    nonce CHAR(32) NOT NULL,
    password VARCHAR(128) NOT NULL,
    status VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    modified_at TIMESTAMP WITH TIME ZONE NOT NULL
);
