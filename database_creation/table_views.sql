\c antisocialnetwork antisocial_admin

CREATE VIEW n_friends_per_user AS
    SELECT u.user_id, u.name, COUNT(f.connection_id) AS n_friends
        FROM users u
             LEFT JOIN friends_with f
                ON (u.user_id = f.user1_id OR u.user_id = f.user2_id)
        GROUP BY u.user_id, u.name
        ORDER BY n_friends DESC; -- Could be useful if we wanted to make a ranking


CREATE VIEW n_likes_per_post AS
    SELECT p.post_id, COUNT(l.user_id) AS n_likes
        FROM posts p
            LEFT JOIN likes l
                 USING (post_id)
        GROUP BY p.post_id;

CREATE VIEW n_comments_per_post AS
    SELECT p.post_id, COUNT(c.user_id) AS n_comments
        FROM posts p
            LEFT JOIN comments c
                 USING (post_id)
        GROUP BY p.post_id;

CREATE VIEW show_posts AS
    SELECT p.post_id, p.title, u.name, p.post_date, nl.n_likes, nc.n_comments
        FROM posts p
            JOIN users u
                 ON (p.author_id = u.user_id)
            JOIN n_comments_per_post nc
                 USING (post_id)
            JOIN n_likes_per_post nl
                 USING (post_id)
        ORDER BY user_id;
