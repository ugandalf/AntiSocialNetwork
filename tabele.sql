CREATE TABLE login_credentials (
    id text NOT NULL,
    email text NOT NULL,
    password text NOT NULL
);

CREATE TABLE users (
    id text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    birth_date date,
    sex text,
    country text
);


CREATE TABLE posts (
    user_id text NOT NULL,
    post_id text NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    date date NOT NULL
);


CREATE TABLE friends_request (
  user_id text NOT NULL,
  user2_id text NOT NULL,
  date date NOT NULL
);


CREATE TABLE tags (
  tags text NOT NULL
);


CREATE TABLE post_tags (
  tag text NOT NULL,
  post_id text NOT NULL
);


CREATE TABLE comments (
    user_id text NOT NULL,
    post_id text NOT NULL,
    content text NOT NULL,
    date date NOT NULL
);


CREATE TABLE likes (
    user_id text NOT NULL,
    post_id text NOT NULL
);


CREATE TABLE interests (
    user_id text NOT NULL,
    tag text NOT NULL
);
