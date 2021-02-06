import datetime
from flask import render_template, request, flash, redirect, url_for, session, make_response, abort

from flask_init import *
from forms.post_form import PostForm
from forms.message_form import MessageForm
from forms.tag_form import TagForm
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
    comment_form = MessageForm(request.form)
    if request.method == 'POST':
        if request.form.get('submit_button', False) == 'Add Like':
            db.session.add(Likes(user_id = u, post_id = post_id))
            db.session.commit()
            flash("Successfully added a like to the post")
            return redirect(url_for('post', post_id = post_id))
        if request.form.get('submit_button', False) == 'Remove Like':
            db.session.delete(liked)
            db.session.commit()
            flash("Successfully removed a like to the post")
            return redirect(url_for('post', post_id = post_id))
        if comment_form.validate():
            comment = Comments(user_id = u,
                               post_id = post_id,
                               comment_date = datetime.datetime.now().replace(microsecond=0),
                               comment = comment_form.message.data)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('post', post_id = post_id))
    return render_template("view_post.html", post_contents = post_contents, post_intro = post_intro,
                           liked = bool(liked), comments = comments, tags = tags, comment_form = comment_form)


@app.route('/messages/<int:friend_id>', methods = ['GET', 'POST'])
def messages(friend_id):
    u = request.cookies.get("user_id")
    connection = Friends_with.query.filter((Friends_with.user1_id == u) | (Friends_with.user2_id == u))
    connection = connection.filter((Friends_with.user1_id == friend_id) | (Friends_with.user2_id == friend_id)).first_or_404()
    message_history = Messages.query.filter_by(connection_id = connection.connection_id).all()
    message_form = MessageForm(request.form)
    if request.method == 'POST' and message_form.validate():
        message = Messages(connection_id = connection.connection_id,
                           message_date = datetime.datetime.now().replace(microsecond=0),
                           message = message_form.message.data,
                           sender_id = u)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('messages', friend_id = friend_id))
    return render_template("messages.html", message_history = message_history, message_form = message_form)


@app.route('/new_post', methods = ['GET', 'POST'])
def new_post():
    u = request.cookies.get("user_id")
    new_post_form = PostForm(request.form).new()
    if request.method == 'POST' and new_post_form.validate():
        post = Posts(title = new_post_form.title.data, content = new_post_form.contents.data, author_id = u,
                     post_date = datetime.datetime.now().replace(microsecond=0))
        db.session.add(post)
        db.session.commit()
        for i in new_post_form.tags.data:
            db.session.add(PostTags(post_id = post.post_id, tag_id = i))
            db.session.commit()
        flash("Post created successfully!")
        return redirect(url_for('post', post_id = post.post_id))
    return render_template("create_post.html", new_post_form = new_post_form)


@app.route('/tags', methods = ['GET', 'POST'])
def tags():
    tags = TagList.query.order_by(TagList.tag).all()
    tag_form = TagForm(request.form)
    if request.method == 'POST':
        if tag_form.validate():
            tag = TagList(tag = tag_form.tag.data)
            db.session.add(tag)
            db.session.commit()
            flash('Tag successfully added!')
    return render_template("tags.html", tags = tags, tag_form = tag_form)


@app.route('/tag/<int:tag_id>', methods = ['GET', 'POST'])
def tag(tag_id):
    u = request.cookies.get("user_id")
    tag = TagList.query.filter_by(tag_id = tag_id).first_or_404()
    is_interest = Interests.query.filter_by(user_id = u).filter_by(tag_id = tag.tag_id).first()
    posts_with_tag = PostTags.query.filter_by(tag_id = tag_id).all()
    users_with_tag = Interests.query.filter_by(tag_id = tag_id).all()
    if request.method == 'POST':
                if request.form['submit_button'] == 'Add interest':
                    db.session.add(Interests(tag_id = tag.tag_id, user_id = u))
                    db.session.commit()
                    flash('Successfully added as an interest')
                if request.form['submit_button'] == 'Remove interest':
                    db.session.delete(is_interest)
                    db.session.commit()
                    flash('Successfully removed as an interest')
                return redirect(url_for('tag', tag_id=tag_id))
    return render_template("tag.html", tag = tag, is_interest = is_interest, posts_with_tag = posts_with_tag, users_with_tag = users_with_tag)


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
