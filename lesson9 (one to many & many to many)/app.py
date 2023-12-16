from flask import render_template
from flask_login import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

from config import app, db
from models import User, Address, Post, Tag
from forms import UserForm, AddressForm


@login_manager.user_loader
def load_user(user_id):
    db_sess = db.session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    users = User.query.all()
    # town = Address.query.filter_by(town_name='город 1').first()
    # print(town)
    # user1 = User(username='Магомед', address=town.id)
    # db.session.add(user1)
    #
    # town1 = Address(town_name='Махачкала')
    # town2 = Address(town_name='Дербент')
    # db.session.add(town1)
    # db.session.add(town2)
    # user2 = User(username='Гасей', address=1)
    # user3 = User(username='Сидредин', address=1)
    # db.session.add(user2)
    # db.session.add(user3)
    # db.session.commit()
    # user2 = User.query.get(4)
    # print(user2.user_address.town_name)
    # address = Address.query.get(1)
    # print([user.username for user in address.users])

    # post1 = Post(post_name='Название 1')
    # post2 = Post(post_name='Название 1')
    #
    # db.session.add(post1)
    # db.session.add(post2)
    #
    # tag1 = Tag(tag_name='тег1')
    # tag2 = Tag(tag_name='тег2')
    #
    # db.session.add(tag1)
    # db.session.add(tag2)
    #
    # db.session.commit()

    post1 = Post.query.get_or_404(6)
    # tag1 = Tag.query.get_or_404(1)
    # tag2 = Tag.query.get_or_404(2)
    #
    # post1.tags.append(tag1)
    # post1.tags.append(tag2)
    #
    # db.session.commit()
    #
    print(post1.tags)
    # print(tag1.posts)
    # print(tag2.posts)

    return render_template('index.html', users=users)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.route('/users', methods=['GET', 'POST'])
def users():
    userForm = UserForm()
    if userForm.validate_on_submit():
        username = userForm.username.data
        hash_password = userForm.password_data
        address = userForm.address.data
        user = User(username=username,
                    hash_password=hash_password,
                    address=address)
        db.session.add(user)
        db.session.commit()

    users = User.query.all()
    return render_template('users.html', users=users, form=userForm)


@app.route('/town', methods=['GET', 'POST'])
def get_towns():
    # user = User.query.filter_by(username=username).first_or_404()

    addressForm = AddressForm()
    if addressForm.validate_on_submit():
        town_name = addressForm.town_name.data
        town = Address(town_name=town_name)
        db.session.add(town)
        db.session.commit()

    towns = Address.query.all()
    return render_template('towns.html', towns=towns, form=addressForm)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='127.0.0.1', debug=True)