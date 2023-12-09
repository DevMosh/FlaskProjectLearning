from config import db


class User(db.Model):
    __tablename__ = 'all_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    usesurname = db.Column(db.String(255), unique=True, nullable=True)
    # Распространенные типы - Integer, String, Text, Boolean, DateTime, Float, LargeBinary

    def __repr__(self):
        return f"<User id={self.id} username={self.username} usesurname={self.usesurname} >"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=True)


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)