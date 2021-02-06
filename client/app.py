from flask import render_template, request, flash, redirect, url_for, session, make_response, abort

from flask_init import *

# routes:
from welcome_page import welcome_page


@app.route('/users', methods=['GET'], defaults={"page": 1})
@app.route('/users/<int:page>', methods=['GET'])
def users(page):
    users = Users.query.paginate(page, per_page=25)
    return render_template("users.html", users = users)

@app.route('/posts', methods=['GET'], defaults={"page": 1})
@app.route('/posts/<int:page>', methods=['GET'])
def posts(page):
    post_pagination = db.session.query("(post_id, title, name, post_date, n_likes, n_comments) FROM show_posts").paginate(page, per_page=15)
    posts = list(map(lambda x: x[0][1:-1].split(','), post_pagination.items))
    return render_template("posts.html", post_pagination = post_pagination, posts = posts)

@app.route('/profile/', methods=['GET', 'POST'], defaults={"user_id": -1})
@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if user_id == -1:
        u = request.cookies.get("user_id")
        return redirect(url_for('profile', user_id=u))
    user = Users.query.filter_by(user_id=user_id).first()
    if user:
        current_user = request.cookies.get("user_id")
        n_friends = db.session.query(f"n_friends FROM n_friends_per_user WHERE user_id = {user_id}").first()[0]
        country = Countries.query.filter_by(country_id = user.country_id).first().country_name
        tags = Interests.query.filter_by(user_id = user_id).with_entities(Interests.tag_id)
        tags = TagList.query.filter(TagList.tag_id.in_(tags)).with_entities(TagList.tag).all()
        if user_id == int(current_user):
            return render_template("your_profile.html", n_friends = n_friends, user = user, country = country, interests = tags)
        else:
            is_friends = Friends_with.query.filter((Friends_with.user1_id == user_id) | (Friends_with.user2_id == user_id))
            is_friends = is_friends.filter((Friends_with.user1_id == current_user) | (Friends_with.user2_id == current_user)).first()
            before_request = Friend_requests.query.filter((Friend_requests.user1_id == user_id) | (Friend_requests.user2_id == user_id))
            before_request = before_request.filter((Friend_requests.user1_id == current_user) | (Friend_requests.user2_id == current_user)).first()
            if request.method == 'POST':
                if request.form['submit_button'] == 'Unfriend':
                    db.session.delete(is_friends)
                    db.session.commit()
                    flash('Unfriended successfully')
                    return redirect(url_for('profile', user_id=user_id))
                if request.form['submit_button'] == 'Send friend request':
                    db.session.add(Friend_requests(user1_id = current_user, user2_id = user_id))
                    db.session.commit()
                    flash('Friend request sent')
                    return redirect(url_for('profile', user_id=user_id))
                if request.form['submit_button'] == 'Remove friend request':
                    db.session.delete(before_request)
                    db.session.commit()
                    flash('Friend request unsent')
                    return redirect(url_for('profile', user_id=user_id))
            is_friends = bool(is_friends)
            before_request = bool(before_request)

            return render_template("profile.html", user = user, n_friends = n_friends, is_friends = is_friends, before_request = before_request,
                                   country = country, interests = tags)
    else:
        return abort(404)

@app.route('/friends', methods=['GET', 'POST'])
def friends():
    u = request.cookies.get("user_id")
    friend_requests = Friend_requests.query.filter_by(user2_id = u).with_entities(Friend_requests.user1_id)
    friend_requests = Users.query.filter(Users.user_id.in_(friend_requests)).all()

    friends1 = Friends_with.query.filter(Friends_with.user1_id == u).with_entities(Friends_with.user2_id)
    friends2 = Friends_with.query.filter(Friends_with.user2_id == u).with_entities(Friends_with.user1_id)
    friends = friends1.union(friends2)
    friends = Users.query.filter(Users.user_id.in_(friends)).all()
    if request.method == 'POST':
        for req in friend_requests:
            if request.form.get('submit_button_' + str(req.user_id), None) == "Delete":
                fr = Friend_requests.query.filter_by(user1_id = req.user_id).filter_by(user2_id = u).first()
                db.session.delete(fr)
                db.session.commit()
                flash("Successfully deleted a friend request ")
                return redirect(url_for('friends'))
            if request.form.get('submit_button_' + str(req.user_id), None) == "Accept":
                db.session.add(Friends_with(user1_id = req.user_id, user2_id = u))
                db.session.commit()
                flash("Successfully accepted a friend request ")
                return redirect(url_for('friends'))
        for fri in friends:
            if request.form.get('submit_button_' + str(fri.user_id), None) == "Message":
                return redirect(url_for('messages', friend_id = fri.user_id))
    return render_template("friends.html", friend_requests = friend_requests, friends = friends)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    u = request.cookies.get("user_id")
    post_contents = Posts.query.filter_by(post_id = post_id).first()
    post_intro = db.session.query("(post_id, title, name, post_date, n_likes, n_comments) FROM show_posts")
    post_intro = list(map(lambda x: x[0][1:-1].split(','), post_intro.all()))
    post_intro = [x for x in post_intro if x[0] == str(post_id)][0][2:]
    liked = Likes.query.filter_by(user_id = u).filter_by(post_id = post_id).first()
    comments = Comments.query.filter_by(post_id = post_id).with_entities(Comments.user_id, Comments.comment, Comments.comment_date).all()
    tags = PostTags.query.filter_by(post_id = post_id).with_entities(PostTags.tag_id)
    tags = TagList.query.filter(TagList.tag_id.in_(tags)).with_entities(TagList.tag).all()
    if request.method == 'POST':
        if request.form['submit_button'] == 'Add Like':
            db.session.add(Likes(user_id = u, post_id = post_id))
            db.session.commit()
            flash("Successfully added a like to the post")
            return redirect(url_for('post', post_id = post_id))
        if request.form['submit_button'] == 'Remove Like':
            db.session.delete(liked)
            db.session.commit()
            flash("Successfully removed a like to the post")
            return redirect(url_for('post', post_id = post_id))
    return render_template("view_post.html", post_contents = post_contents, post_intro = post_intro,
                           liked = bool(liked), comments = comments, tags = tags)

@app.route('/messages/<int:friend_id>')
def messages(friend_id):
    u = request.cookies.get("user_id")
    connection = Friends_with.query.filter((Friends_with.user1_id == u) | (Friends_with.user2_id == u))
    connection = connection.filter((Friends_with.user1_id == friend_id) | (Friends_with.user2_id == friend_id)).first_or_404()
    message_history = Messages.query.filter_by(connection_id = connection.connection_id).all()
    return render_template("messages.html", message_history = message_history)


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
