\c antisocialnetwork antisocial_admin

-- if the user changes user_id, it changes globally
ALTER TABLE users
    ADD CONSTRAINT fkey_user_id
    FOREIGN KEY (user_id)
    REFERENCES login_credentials(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- you can't delete a country someone lives in
-- when you change country_id in countries, it changes here
ALTER TABLE users
    ADD CONSTRAINT fkey_country_id
    FOREIGN KEY (country_id)
    REFERENCES countries(country_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- when the user quits, we delete all the post they have
-- when the user changes id, it changes in the post
ALTER TABLE posts
    ADD CONSTRAINT fkey_author_id
    FOREIGN KEY (author_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- friendship or friend request can't exist without a user
ALTER TABLE friend_requests
    ADD CONSTRAINT fkey_user1_id
    FOREIGN KEY (user1_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE friend_requests
    ADD CONSTRAINT fkey_user2_id
    FOREIGN KEY (user2_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE friends_with
    ADD CONSTRAINT fkey_user1_id
    FOREIGN KEY (user1_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE friends_with
    ADD CONSTRAINT fkey_user2_id
    FOREIGN KEY (user2_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- when a connection_id gets renamed, it gets renamed in a message
-- we delete messages who are no longer friends
-- so that nobody stumbles upon it
ALTER TABLE messages
    ADD CONSTRAINT fkey_connection_id
    FOREIGN KEY (connection_id)
    REFERENCES friends_with(connection_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- we can't delete a tag if there is a post which contains it
-- we can however update its id to be the correct one
ALTER TABLE post_tags
    ADD CONSTRAINT fkey_tag_id
    FOREIGN KEY (tag_id)
    REFERENCES tag_list(tag_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;

-- when we delete a post we delete the connection
-- when we update post_id, we update its list of tags
ALTER TABLE post_tags
    ADD CONSTRAINT fkey_post_id
    FOREIGN KEY (post_id)
    REFERENCES posts(post_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- existence of comment relies on existence of post and user
ALTER TABLE comments
    ADD CONSTRAINT fkey_post_id
    FOREIGN KEY (post_id)
    REFERENCES posts(post_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE comments
    ADD CONSTRAINT fkey_user_id
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- likes aren't more important than users or posts
ALTER TABLE likes
    ADD CONSTRAINT fkey_user_id
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE likes
    ADD CONSTRAINT fkey_post_id
    FOREIGN KEY (post_id)
    REFERENCES posts(post_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- users are more important than interests
ALTER TABLE interests
    ADD CONSTRAINT fkey_user_id
    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- we can't delete a tag if someone is interested in it
ALTER TABLE interests
    ADD CONSTRAINT fkey_tag_id
    FOREIGN KEY (tag_id)
    REFERENCES tag_list(tag_id)
    ON DELETE RESTRICT
    ON UPDATE CASCADE;
