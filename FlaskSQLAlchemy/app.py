# миграции
# установить библиотеку

from flask import render_template, redirect, url_for, request
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from config import app, db
from forms import PostForm
from models import User, Post

migrate = Migrate(app, db, render_as_batch=True)


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    usesurname = request.form.get('usesurname')
    user = User(username=username, usesurname=usesurname)
    db.session.add(user)
    db.session.commit()
    print(user)
    return redirect(url_for('index'))


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    postform = PostForm()
    if request.method == 'POST':

        if postform.validate_on_submit():
            # title = request.form.get('title')
            # text = request.form.get('text')
            # author = request.form.get('author')

            title = postform.title.data
            text = postform.text.data
            author = postform.author.data

            post = Post(title=title, text=text, author=author)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('posts'))
    else:
        posts = Post.query.all()
        return render_template('posts.html', posts=posts, form=postform)


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    return render_template('single_post.html', post=post)


@app.route('/posts/author/<string:author_name>')
def get_posts_author(author_name):
    posts = Post.query.filter_by(author=author_name)
    print(posts)
    return render_template('author_posts.html', posts=posts)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='127.0.0.1', debug=True)
