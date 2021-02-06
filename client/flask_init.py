from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://antisocial_admin@localhost/antisocialnetwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "\x0el\t[\xa9\xb6\x9f\xe9\x00\x08m\x99C\xd51'l\x9d\x93\xc9\x82bv\xcd"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

db.Model.metadata.reflect(db.engine, views = True)

class Users(db.Model):
    __table__ = db.Model.metadata.tables['users']

class LoginCredentials(db.Model):
    __table__ = db.Model.metadata.tables['login_credentials']

class Countries(db.Model):
    __table__ = db.Model.metadata.tables['countries']

class Posts(db.Model):
    __table__ = db.Model.metadata.tables['posts']

class Friends_with(db.Model):
    __table__ = db.Model.metadata.tables['friends_with']

class Friend_requests(db.Model):
    __table__ = db.Model.metadata.tables['friend_requests']

class Likes(db.Model):
    __table__ = db.Model.metadata.tables['likes']

class Messages(db.Model):
    __table__ = db.Model.metadata.tables['messages']

class Comments(db.Model):
    __table__ = db.Model.metadata.tables['comments']

class PostTags(db.Model):
    __table__ = db.Model.metadata.tables['post_tags']

class Interests(db.Model):
    __table__ = db.Model.metadata.tables['interests']

class TagList(db.Model):
    __table__ = db.Model.metadata.tables['tag_list']

country_list = list(map(lambda x: x[0], db.session.query(Countries.country_name).order_by('country_name').all()))
