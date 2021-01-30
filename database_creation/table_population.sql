\c antisocialnetwork antisocial_admin

CREATE OR REPLACE PROCEDURE populate_countries()
LANGUAGE plpython3u
AS $$
    from faker import Faker, exceptions
    fake = Faker()
    countrylist = []
    while True:
        try:
            countrylist.append(fake.unique.country())
        except exceptions.UniquenessException:
            break
    plan = plpy.prepare("INSERT INTO countries(country_name) VALUES ($1)", ["VARCHAR(51)"])
    for i in countrylist:
        plan.execute([i])
$$;


CREATE OR REPLACE PROCEDURE generate_users(n_users INTEGER)
LANGUAGE plpython3u
AS $$
    from faker import Faker
    fake = Faker()

    stock_genders = {'male': fake.name_male,
                   'female': fake.name_female,
               'trans male': fake.name_male,
             'trans female': fake.name_female,
                'nonbinary': fake.name_nonbinary}

    # COALESCE returns first not null argument
    START_USER_ID = plpy.execute("SELECT COALESCE(MAX(user_id) + 1, 1) FROM users")[0]["coalesce"]
    user_birthdays = [fake.date_of_birth(minimum_age=18, maximum_age=60) for _ in range(n_users)]
    user_genders = fake.random_choices(stock_genders.keys(), n_users)
    user_names = list(map(lambda x: stock_genders[x](), user_genders))
    MAX_COUNTRY_ID = plpy.execute("SELECT COUNT(*) FROM countries")[0]["count"]
    user_countries = [fake.random_int(min=1, max=MAX_COUNTRY_ID) for _ in range(n_users)]

    plan = plpy.prepare("INSERT INTO login_credentials(email, password) VALUES ($1, $2)", ["VARCHAR(254)", "VARCHAR(53)"])
    for i in range(n_users):
        curr_id = i + START_USER_ID
        username = ".".join(user_names[i].split()) + str(curr_id)
        email = f"{username}@gmail.com"
        password = f"{username}_123"
        plan.execute([email, password])
    plan = plpy.prepare("INSERT INTO users(user_id, name, birthday, gender, country_id) VALUES ($1, $2, $3, $4, $5)",
                                          ["INTEGER", "VARCHAR(255)", "DATE", "VARCHAR(32)", "INTEGER"])
    for i in range(n_users):
        plan.execute([i + START_USER_ID, user_names[i], user_birthdays[i], user_genders[i], user_countries[i]])
$$;


CREATE OR REPLACE PROCEDURE generate_friendships(p FLOAT, q FLOAT)
LANGUAGE plpython3u
AS $$
    from random import random
    pairs = plpy.execute("SELECT u1.user_id AS user1, u2.user_id AS user2 FROM users u1, users u2 WHERE u1.user_id < u2.user_id")
    plan1 = plpy.prepare("INSERT INTO friend_requests(user1_id, user2_id) VALUES ($1, $2)", ["INTEGER", "INTEGER"])
    plan2 = plpy.prepare("INSERT INTO friends_with(user1_id, user2_id) VALUES ($1, $2)", ["INTEGER", "INTEGER"])
    for row in pairs:
        v = random()
        if v < p:  # rolled friend request
            u1 = row["user1"]
            u2 = row["user2"]
            u = [u1, u2] if random() < 0.5 else [u2, u1]
            plan1.execute(u)
            if v < q: # rolled that it got accepted - deletion of request handled in a trigger
                plan2.execute(u)
$$;


CREATE OR REPLACE PROCEDURE generate_messages(n_connections INTEGER, n_messages_per INTEGER)
LANGUAGE plpython3u
AS $$
    from faker import Faker
    import datetime
    fake = Faker()
    plan = plpy.prepare("SELECT * FROM friends_with ORDER BY RANDOM() LIMIT $1", ["INTEGER"])
    connections = plan.execute([n_connections])
    plan = plpy.prepare("INSERT INTO messages(connection_id, message_date, message, sender_id) VALUES ($1, $2, $3, $4)",
                                             ["INTEGER", "TIMESTAMP", "TEXT", "INTEGER"])
    for row in connections:
        message_date = fake.date_time_this_month()
        for i in range(n_messages_per):
            sender_id = row["user" + str(fake.pybool() + 1) + "_id"]
            message_date += datetime.timedelta(seconds = fake.random_digit_not_null())
            message = fake.sentence(5)
            plan.execute([row["connection_id"], message_date, message, sender_id])
$$;


CREATE OR REPLACE PROCEDURE generate_tags(n_tags INTEGER)
LANGUAGE plpython3u
AS $$
    from faker import Faker
    fake = Faker()
    plan = plpy.prepare("INSERT INTO tag_list(tag) VALUES ($1)", ["VARCHAR(32)"])
    for _ in range(n_tags):
        tag = fake.unique.word()
        plan.execute([tag])
$$;


CREATE OR REPLACE PROCEDURE generate_posts_with_comments(n_posts INTEGER, n_comments_per INTEGER, p FLOAT)
LANGUAGE plpython3u
AS $$
    from faker import Faker
    import datetime
    fake = Faker()

    MAX_USER_ID = plpy.execute("SELECT COUNT(*) FROM users")[0]["count"]
    post_tags_plan = plpy.prepare("INSERT INTO post_tags(tag_id, post_id) VALUES ($1, $2)", ["INTEGER", "INTEGER"])
    post_plan = plpy.prepare("INSERT INTO posts(author_id, title, content, post_date) VALUES ($1, $2, $3, $4)",
                                          ["INTEGER", "VARCHAR(70)", "TEXT", "TIMESTAMP"])
    comment_plan = plpy.prepare("INSERT INTO comments(user_id, post_id, comment, comment_date) VALUES ($1, $2, $3, $4)",
                                ["INTEGER", "INTEGER", "TEXT", "TIMESTAMP"])
    # A user with a specific interest creates a post about that interest
    post_id = plpy.execute("SELECT COALESCE(MAX(post_id) + 1, 1) FROM posts")[0]["coalesce"]
    author_id_plan = plpy.prepare("SELECT user_id, tag_id FROM interests ORDER BY RANDOM() LIMIT $1", ["INTEGER"])
    for row in author_id_plan.execute([n_posts]):
        # First we generate the post itself
        author_id = row["user_id"]
        title = fake.sentence(4)
        content = fake.paragraph()
        post_date = fake.date_time_this_month()
        post_plan.execute([author_id, title, content, post_date])
        # Next we generate post_tags
        post_tags_plan.execute([row["tag_id"], post_id])
        # Then come comments
        for _ in range(n_comments_per):
            user_id = fake.random_int(min=1, max=MAX_USER_ID)
            comment = fake.sentence(4)
            post_date += datetime.timedelta(minutes = fake.random_digit_not_null())
            comment_plan.execute([user_id, post_id, comment, post_date])
            # and likes
            b_already_liked = (plpy.execute(f"SELECT COUNT(*) FROM likes WHERE user_id = {user_id} AND post_id = {post_id}")[0]["count"] > 0)
            if fake.random.random() < p and not b_already_liked:
               like_plan = plpy.prepare("INSERT INTO likes(user_id, post_id) VALUES ($1, $2)", ["INTEGER", "INTEGER"])
               like_plan.execute([user_id, post_id])
        # and then we generate next post
        post_id += 1
$$;


CREATE OR REPLACE PROCEDURE generate_interests(n_interests_per_user INTEGER)
LANGUAGE plpython3u
AS $$
    from random import sample;
    user_ids = plpy.execute("SELECT user_id FROM users")
    tag_ids = plpy.execute("SELECT tag_id FROM tag_list")
    plan = plpy.prepare("INSERT INTO interests VALUES ($1, $2)", ["INTEGER", "INTEGER"])
    for user in user_ids:
        sample(range(tag_ids.nrows()), n_interests_per_user)
        for interest in sample(range(tag_ids.nrows()), n_interests_per_user):
            plan.execute([user["user_id"], tag_ids[interest]["tag_id"]])
$$;
