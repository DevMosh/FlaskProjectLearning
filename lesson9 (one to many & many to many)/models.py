from flask_login import UserMixin
from config import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    hash_password = db.Column(db.Text, nullable=False)
    address = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    town_name = db.Column(db.Text, unique=True, nullable=False)
    users = db.relationship('User', backref='user_address')


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.Text, nullable=False)
    tags = db.relationship('Tag', backref='posts', secondary='post_tag')


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text, nullable=False)


post_tag = db.Table(
    'post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
)