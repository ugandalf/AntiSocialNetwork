\c antisocialnetwork antisocial_admin

CALL populate_countries();
CALL generate_users(200);
-- ln(n) / n = 0.026... => connectedness threshold
CALL generate_friendships(0.03, 0.0259);
CALL generate_messages(50, 4);
CALL generate_tags(100);
CALL generate_interests(3);
CALL generate_posts_with_comments(20, 4, 0.5)
