\c antisocialnetwork antisocial_admin

ALTER TABLE login_credentials
    ADD CONSTRAINT pkey_login_credentials
    PRIMARY KEY (user_id);

ALTER TABLE users
    ADD CONSTRAINT pkey_users
    PRIMARY KEY (user_id);

ALTER TABLE countries
    ADD CONSTRAINT pkey_countries
    PRIMARY KEY (country_id);

ALTER TABLE posts
    ADD CONSTRAINT pkey_posts
    PRIMARY KEY (post_id);

ALTER TABLE friend_requests
    ADD CONSTRAINT pkey_friend_requests
    PRIMARY KEY (connection_id);

ALTER TABLE friends_with
    ADD CONSTRAINT pkey_friends_with
    PRIMARY KEY (connection_id);

ALTER TABLE messages
    ADD CONSTRAINT pkey_messages
    PRIMARY KEY (connection_id, message_date, sender_id);

ALTER TABLE tag_list
    ADD CONSTRAINT pkey_tag_list
    PRIMARY KEY (tag_id);

ALTER TABLE post_tags
    ADD CONSTRAINT pkey_post_tags
    PRIMARY KEY (tag_id, post_id);

ALTER TABLE comments
    ADD CONSTRAINT pkey_comments
    PRIMARY KEY (user_id, post_id, comment_date);

ALTER TABLE likes
    ADD CONSTRAINT pkey_likes
    PRIMARY KEY (user_id, post_id);

ALTER TABLE interests
    ADD CONSTRAINT pkey_interests
    PRIMARY KEY (user_id, tag_id);
