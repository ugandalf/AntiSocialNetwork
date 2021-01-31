from flask import render_template, request, flash, redirect, url_for, session, make_response, abort

from flask_init import *

# routes:
from welcome_page import welcome_page


@app.route('/users', methods=['GET'], defaults={"page": 1})
@app.route('/users/<int:page>', methods=['GET'])
def users(page):
    users = Users.query.paginate(page, per_page=50)
    return render_template("users.html", users = users)

@app.route('/posts', methods=['GET'])
def posts():
    return render_template("posts.html")

@app.route('/profile/', methods=['GET'], defaults={"user_id": -1})
@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    if user_id == -1:
        u = request.cookies.get("user_id")
        return redirect(url_for('profile', user_id=u))
    user = Users.query.filter_by(user_id=user_id).first()
    if user:
        return render_template("profile.html", user = user)
    else:
        return abort(404)

@app.route('/logout')
def logout():
    u = request.cookies.get("user_id")
    if session.get(u, False):
        resp = make_response(redirect(url_for("welcome_page")))
        session.pop(u, None)
        resp.set_cookie('user_id', '', expires=0)
        flash("Logged out successfully")
        return resp
    user = Users.query.filter_by(user_id=user_id).first()
    if user:
        return render_template("profile.html", user = user)
    else:
        return abort(404)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host= '0.0.0.0')
