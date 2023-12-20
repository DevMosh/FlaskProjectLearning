from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from config import login_manager

from config import app, db
from models import User
from forms import UserForm, LoginForm


@login_manager.user_loader
def load_user(user_id):
    # db_sess = db.session.create_session()
    # return db_sess.query(User).get(user_id)
    return User.query.get(user_id)
    # return db.session.execute(db.)


@app.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    username = login_form.username.data
    password = login_form.password.data
    user = User.query.filter_by(username=username).first()
    # if user and User.hash_password == password:
    if user and check_password_hash(user.hash_password, password):
        login_user(user)
        return redirect(url_for('user_info'))
    else:
        return render_template('index.html',
                               form=login_form,
                               fatal_auth=True)

    return render_template('index.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user_info')
@login_required
def user_info():
    return render_template('user_info.html', name_user=current_user.username)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error), 404


@app.errorhandler(401)
def page_not_found(error):
    return render_template('401.html', error=error), 401


@app.route('/users', methods=['GET', 'POST'])
def users():
    userForm = UserForm()
    if userForm.validate_on_submit():
        username = userForm.username.data
        hash_password = generate_password_hash(userForm.password.data)
        user = User(username=username,
                    hash_password=hash_password)
        db.session.add(user)
        db.session.commit()

    users = User.query.all()
    return render_template('users.html', users=users, form=userForm)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='127.0.0.1', debug=True)