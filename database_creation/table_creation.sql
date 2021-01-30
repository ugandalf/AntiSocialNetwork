\c antisocialnetwork antisocial_admin

CREATE TABLE login_credentials (
    user_id SERIAL NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    password VARCHAR(53) NOT NULL
);

CREATE TABLE users (
    user_id INTEGER,
    name VARCHAR(255) NOT NULL,
    birthday DATE NOT NULL,
    gender VARCHAR(32),
    country_id INTEGER
);

CREATE TABLE countries (
    country_id SERIAL,
    country_name VARCHAR(51) NOT NULL
);

CREATE TABLE posts (
    post_id SERIAL NOT NULL,
    author_id INTEGER NOT NULL,
    title VARCHAR(70) NOT NULL,
    content TEXT NOT NULL,
    post_date TIMESTAMP NOT NULL
);


CREATE TABLE friend_requests (
    connection_id SERIAL,
    user1_id INTEGER NOT NULL,
    user2_id INTEGER NOT NULL
);


CREATE TABLE friends_with (
    connection_id SERIAL,
    user1_id INTEGER,
    user2_id INTEGER
);

CREATE TABLE messages (
    connection_id INTEGER,
    message_date TIMESTAMP,
    message TEXT,
    sender_id INTEGER
);


CREATE TABLE tag_list (
  tag_id SERIAL,
  tag VARCHAR(32) NOT NULL
);


CREATE TABLE post_tags (
  tag_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL
);


CREATE TABLE comments (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    comment_date TIMESTAMP NOT NULL
);


CREATE TABLE likes (
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL
);


CREATE TABLE interests (
    user_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL
);
