# pip install flask-wtf
import os

from flask import Flask
from flask import render_template, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.getenv("MY_SECRET_KEY"))
csrf = CSRFProtect(app)

class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = StringField('Submit')


@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        print(name, text)
        return redirect('/success')
        # return redirect(url_for('success'))
    return render_template('add_post.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        print(name, email, password)
        return redirect('/success')
        # return redirect(url_for('success'))


    return render_template('home.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)