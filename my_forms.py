# pip install flask-wtf
import os
import sqlite3

from flask import Flask
from flask import render_template, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, DateField
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


class AddNewsForm(FlaskForm):
    name = StringField('Имя автора', validators=[DataRequired()])
    name_news = StringField('Название новости', validators=[DataRequired()])
    text = StringField('Текст новости')
    email = EmailField('Почта ( хз зачем )', validators=[DataRequired()])
    date = DateField('Дата публикации ( тоже хз зачем )', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/add-news', methods=['GET', 'POST'])
def add_news():
    form = AddNewsForm()
    if form.validate_on_submit():
        name = form.name.data
        name_news = form.name_news.data
        text = form.text.data
        email = form.email.data
        date = form.date.data


        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO news (name, content) VALUES (?, ?)',
                       (name, text))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect('/')
    return render_template('add_news.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def home():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    news = cursor.execute("SELECT * FROM news").fetchall()
    cursor.close()
    connection.close()

    return render_template('home.html', news=news)


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

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     form = MyForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         password = form.password.data
#         print(name, email, password)
#         return redirect('/success')
#         # return redirect(url_for('success'))

    # return render_template('home.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)