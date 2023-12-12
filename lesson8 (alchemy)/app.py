from flask import render_template
from config import app, db
from models import User
from forms import UserForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    userForm = UserForm()
    if userForm.validate_on_submit():
        username = userForm.username.data
        address = userForm.address.data
        age = userForm.age.data

        user = User(username=username, address=address, age=age)
        db.session.add(user)
        db.session.commit()

    users = User.query.all()
    return render_template('users.html', users=users, form=userForm)


@app.route('/spec_users', methods=['GET'])
def spec_users():
    userForm = UserForm()
    users = User.query.all()
    return render_template('users.html', users=users, form=userForm)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, host='127.0.0.1', debug=True)