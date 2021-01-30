\c antisocialnetwork antisocial_admin

CREATE VIEW n_friends_per_user AS
    SELECT u.user_id, u.name, COUNT(f.connection_id) AS n_friends
        FROM users u
             JOIN friends_with f
                ON (u.user_id = f.user1_id OR u.user_id = f.user2_id)
        GROUP BY u.user_id, u.name
        ORDER BY n_friends DESC;
