\c antisocialnetwork antisocial_admin

CREATE OR REPLACE FUNCTION validate_email()
RETURNS TRIGGER
AS $$
  # Possible improvement: check lengths of each part
  import re
  email = TD["new"]["email"]
  # used "https://emailregex.com/"
  p = re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
  if p.match(email):
     return "OK"
  else:
     plpy.error('Invalid email format')
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION password_encode(password text)
RETURNS VARCHAR(53)
AS $$
  import bcrypt
  pwd = password.encode()
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(pwd, salt)
  hashed = hashed[7:] # we get rid of "$2b$12$"
  return hashed.decode()
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION password_check(plaintext text, hashed VARCHAR(53))
RETURNS BOOLEAN
AS $$
  import bcrypt
  p2 = b'$2b$12$' + hashed.encode()
  return bcrypt.checkpw(plaintext.encode(), p2)
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION validate_and_hash_password()
RETURNS TRIGGER
AS $$
  import re
  pwd = TD["new"]["password"]
  p = re.compile('(^[a-zA-Z0-9_.+-]+$)')
  if p.match(pwd):
     TD["new"]["password"] = plpy.execute(f"SELECT password_encode('{pwd}')")[0]["password_encode"]
     return "MODIFY"
  else:
     plpy.error("Password contains illegal character")
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION message_after_births()
RETURNS TRIGGER
AS $$
  message_date = TD["new"]["message_date"]
  sender_id = TD["new"]["sender_id"]
  connection_id = TD["new"]["connection_id"]
  conditions = f"((user1_id = '{sender_id}' OR user2_id = '{sender_id}') AND connection_id = '{connection_id}')"
  row = plpy.execute(f"SELECT * FROM friends_with WHERE {conditions}")[0]
  u1 = row["user1_id"]
  u2 = row["user2_id"]
  for u in [u1, u2]:
      conditions = f"(user_id = '{u}' AND birthday < '{message_date}')"
      r = plpy.execute(f"SELECT * FROM users WHERE {conditions}")
      if r.nrows() != 1:
          plpy.error("Message sent before a user was born!")
  return "OK"
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION posts_after_births()
RETURNS TRIGGER
AS $$
  post_date = TD["new"]["post_date"]
  author_id = TD["new"]["author_id"]
  conditions = f"(user_id = '{author_id}' AND birthday < '{post_date}')"
  r = plpy.execute(f"SELECT * FROM users WHERE {conditions}")
  if r.nrows() == 1:
     return "OK"
  else:
     plpy.error("Post created before a user was born!")
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION comments_after_posts()
RETURNS TRIGGER
AS $$
  comment_date = TD["new"]["comment_date"]
  post_id = TD["new"]["post_id"]
  conditions = f"(post_id = '{post_id}' AND post_date < '{comment_date}')"
  r = plpy.execute(f"SELECT * FROM posts WHERE {conditions}")
  if r.nrows() == 1:
     return "OK"
  else:
     plpy.error("Comment created before a post was born!")
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION delete_requests_after_friendship()
RETURNS TRIGGER
AS $$
  u1 = TD["new"]["user1_id"]
  u2 = TD["new"]["user2_id"]
  plpy.execute(f"DELETE FROM friend_requests WHERE user1_id = '{u1}' AND user2_id = '{u2}';")
$$ LANGUAGE plpython3u;


CREATE OR REPLACE FUNCTION message_in_connection()
RETURNS TRIGGER
AS $$
  connection_id = TD["new"]["connection_id"]
  sender_id = TD["new"]["sender_id"]
  conditions = f"((user1_id = '{sender_id}' OR user2_id = '{sender_id}') AND connection_id = '{connection_id}')"
  r = plpy.execute(f"SELECT * FROM friends_with WHERE {conditions}")
  if r.nrows() == 1:
    return "OK"
  else:
    plpy.error("Sender not friends with the recipient!!!")
$$ LANGUAGE plpython3u;



CREATE TRIGGER handle_passwords
    BEFORE UPDATE OF password OR INSERT
    ON login_credentials
    FOR EACH ROW
    EXECUTE PROCEDURE validate_and_hash_password();


CREATE TRIGGER request_to_friends_transition
    AFTER INSERT
    ON friends_with
    FOR EACH ROW
    EXECUTE PROCEDURE delete_requests_after_friendship();

