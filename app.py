# CGI
# WSGI
# WERKZEUG
# JINJA2

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)  # создается объект приложения


# connection = sqlite3.connect('my_database.db')
# connection.close()
# cursor.execute('''
#         CREATE TABLE IF NOT EXISTS Users (
#         name TEXT NOT NULL,
#         password TEXT NOT NULL
#         )
#         ''')

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS News (
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        ''')


@app.route('/')
@app.route('/home.html')
def hello_world():  # put application's code here
    return render_template('home.html')


@app.route('/about')
def about_site():
    return render_template('news.html')


@app.route('/users/<username>')
def username_info(username):
    return f"{username}"


@app.route('/posts/<int:id>')
def post(id):
    return f"{id}"


# можно явно задавать принимаемые запросы
# @app.route('/login', methods=['POST', 'GET'])
# def login_func():
#     if request.method == 'GET':
#         return render_template('auth.html')
#     elif request.method == 'POST':
#         return '<b> поздравляю, вы авторизировались </b>', 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        user = cursor.execute(f"SELECT * FROM Users WHERE name=?", (request.form.get('login'), )).fetchone()
        print(user)
        cursor.close()
        connection.close()
        if user == None:
            return 'пользователя не существует'

        if user[1] == request.form.get('pass'):
            return 'форма заполнена успешно'
        return 'пароль не правильный'  # обязательно что-нибудь возвращаем
    else:
        return render_template('auth.html')  # форма авторизации


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        print(request.form.get('login'))  # достаем логин, который ввел пользователь
        print(request.form.get('pass'))   # после достаем пароль
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (name, password) VALUES (?, ?)',
                       (request.form.get('login'), request.form.get('pass')))
        connection.commit()
        cursor.close()
        connection.close()

        return 'спасибо за регистрацию'
    else:
        return render_template('registration.html')  # форма авторизации


@app.route("/all-news")
def all_news_func():
    return 'тут будут все новости от всех авторов этого сайта'

@app.route("/all-author")
def all_author_func():
    return 'тут будут все зарегистрированные авторы этого сайта'


@app.route('/add-news', methods=['POST', 'GET'])
def add_news_func():
    if request.method == 'POST':
        print(request.form.get('author'))  # достаем логин, который ввел пользователь
        print(request.form.get('content'))  # после достаем пароль
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO Users (name, password) VALUES (?, ?)',
                       (request.form.get('login'), request.form.get('pass')))
        connection.commit()
        cursor.close()
        connection.close()

        return 'спасибо за регистрацию'
    else:
        return render_template('add_news.html')



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="127.0.0.1", port=80)
    # Устанавливаем соединение с базой данных
