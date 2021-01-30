from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
#from flask_login import LoginManager, UserMixin, login_user

from forms.register_form import RegistrationForm
from forms.login_form import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://antisocial_admin@localhost/antisocialnetwork'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "\x0el\t[\xa9\xb6\x9f\xe9\x00\x08m\x99C\xd51'l\x9d\x93\xc9\x82bv\xcd"
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
#login_manager = LoginManager(app)

# Allows queries from existing tables
db.Model.metadata.reflect(db.engine)

class Users(db.Model):
    __table__ = db.Model.metadata.tables['users']

@app.route('/', methods=['GET', 'POST'])
def base():
    registration_form = RegistrationForm(request.form)
    login_form = LoginForm(request.form)
    if request.method == 'POST' and registration_form.validate():
        flash('Thanks for registering!')
        return redirect(url_for('welcome'))

    if request.method == 'POST' and login_form.validate():

        flash('Thanks for visiting us again!')
        return redirect(url_for('welcome'))

    return render_template("base.html", registration_form = registration_form, login_form = login_form)


@app.route('/welcome', methods=['GET'], defaults={"page": 1})
@app.route('/welcome/<int:page>', methods=['GET'])
def welcome(page):
    users = Users.query.paginate(page, per_page=50)
    return render_template("welcome.html", users = users)

@app.route('/posts', methods=['GET'])
def posts():
    return render_template("posts.html")

#@app.route('/users/<int:user_id>', methods=['GET'])
#def user(user_id):
#    user_row = Users.query.filter_by(user_id = user_id).first_or_404()

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host= '0.0.0.0')
