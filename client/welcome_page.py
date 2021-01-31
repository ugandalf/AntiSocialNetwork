from flask import render_template, request, flash, redirect, url_for, session, make_response

from flask_init import *
from forms.register_form import RegistrationForm
from forms.login_form import LoginForm

@app.route('/', methods=['GET', 'POST'])
def welcome_page():
    # We check if the user is already logged in
    user_id = request.cookies.get('user_id')
    if user_id is not None and session.get(user_id, False):
        return redirect(url_for('posts'))
    registration_form = RegistrationForm(request.form)
    login_form = LoginForm(request.form)

    if request.method == 'POST' and registration_form.validate():
        credentials = LoginCredentials(email = registration_form.email.data, password = registration_form.password.data)
        try:
            db.session.add(credentials)
            db.session.commit()
        except Exception as e:
            print(e.message)
            flash('Registration unsuccessful - email already used (or something unpredictable happened) :/')
        else:
            user = Users(user_id = credentials.user_id,
                         name = registration_form.name.data,
                         birthday = registration_form.birthday.data,
                         gender = registration_form.gender.data,
                         country_id = db.session.query(Countries.country_id).filter_by(country_name=registration_form.country.data).first()[0]
                         )
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can use login below')
        return redirect(url_for('welcome_page'))

    elif request.method == 'POST' and login_form.validate():
        credentials = db.session.query(LoginCredentials).filter_by(email = login_form.email.data).first()
        correct = db.session.execute(f"SELECT password_check('{login_form.password.data}', '{credentials.password}')").first()[0]
        if correct:
            session[str(credentials.user_id)] = True
            resp = make_response(redirect(url_for("posts")))
            # resp.set_cookie('user_id', credentials.user_id.to_bytes(6, 'little'))
            resp.set_cookie('user_id', str(credentials.user_id))
            flash('Thanks for visiting us again!')
            return resp
        else:
            flash('Incorrect email or password!')
            return redirect(url_for('welcome_page'))

    return render_template("welcome.html", registration_form = registration_form, login_form = login_form)
