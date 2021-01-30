\c antisocialnetwork antisocial_admin

ALTER TABLE users
    ADD CONSTRAINT birthday_adult
    CHECK (birthday <= (CURRENT_DATE - INTERVAL '18 years'));

ALTER TABLE friends_with
    ADD CONSTRAINT not_reflexive
    CHECK (user1_id != user2_id);

ALTER TABLE friend_requests
    ADD CONSTRAINT not_reflexive
    CHECK (user1_id != user2_id);

CREATE TRIGGER check_post_date
    BEFORE UPDATE OF post_date OR INSERT
    ON posts
    FOR EACH ROW
    EXECUTE PROCEDURE posts_after_births();

CREATE TRIGGER check_comment_date
    BEFORE UPDATE OF comment_date OR INSERT
    ON comments
    FOR EACH ROW
    EXECUTE PROCEDURE comments_after_posts();

CREATE TRIGGER check_message_between_friends
    BEFORE UPDATE OR INSERT
    ON messages
    FOR EACH ROW
    EXECUTE PROCEDURE message_in_connection();

CREATE TRIGGER check_messages
    BEFORE UPDATE OF message_date OR INSERT
    ON messages
    FOR EACH ROW
    EXECUTE PROCEDURE message_after_births();

CREATE TRIGGER check_email
    BEFORE UPDATE OF email OR INSERT
    ON login_credentials
    FOR EACH ROW
    EXECUTE PROCEDURE validate_email();

-- TODO: Possibly check that friendships and friend_requests are unique regardless of connection_id
