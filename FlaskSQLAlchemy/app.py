from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'all_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    # Распространенные типы - Integer, String, Text, Boolean, DateTime, Float, LargeBinary

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form.get('username')
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    print(user)
    return redirect(url_for('index'))


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        post = Post(title=title, text=text)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts'))
    else:
        posts = Post.query.all()
        return render_template('posts.html', posts=posts)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='127.0.0.1', debug=True)
