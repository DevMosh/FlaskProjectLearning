# CGI
# WSGI
# WERKZEUG
# JINJA2

from flask import Flask, render_template, request, url_for, redirect
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
        CREATE TABLE IF NOT EXISTS Users (
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        ''')
cursor.execute('''
        CREATE TABLE IF NOT EXISTS News (
        name TEXT NOT NULL,
        content TEXT NOT NULL
        )
        ''')
cursor.close()
connection.close()


@app.route('/about')
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
@app.route("/all-news/<string:login>")
def all_news_func(login=None):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    print(cursor.execute("SELECT * FROM users WHERE name=?", (login, )).fetchone())

    news = []
    if login == None:
        text_author = ''
        news = cursor.execute("SELECT * FROM news").fetchall()
    else:
        news = cursor.execute("SELECT * FROM news WHERE name=?", (login, )).fetchall()
        text_author = f'FROM THE AUTHOR {login}'
    news_block = ""

    print(news)

    if news == []:
        news_block += f'<h1>У автора нет новостей</h1>'
    else:
        for i in news:
            news_block += f'<div class="news-block">{i[1]}</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="{ url_for('static', filename='css/home.css') }">
</head>
<body>
    <header>
    <div>
       <div class="logo">
        <a href="home.html">
          <span class="use">NEWS</span>-<span class="web">NEWS</span>.ru
        </a>
       </div>


       <div class="top-menu">
         <ul>
             <li><a class="clickMenu" href="/all-news">Все новости</a></li>
             <li><a href="/all-author">Все авторы</a></li>
             <li><a href="/add-news">Добавить новость</a></li>
         </ul>
       </div>


       <div class="block-top-auth">
         <p><a href="/login">Вход</a></p>
         <p><a href="/registration">Регистрация</a></p>
       </div>

    </header>

    <br>
    <h1 style="text-align: center;">ALL NEWS {text_author}</h1>
    <br>
    <hr>
    <div>
    
    {news_block}

</body>
</html>"""


    return html

@app.route("/all-author")
def all_author_func():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    news = cursor.execute("SELECT * FROM users").fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    print(news)
    news_block = ""
    for i in news:
        news_block += f'<a href="/all-news/{i[0]}"><div class="authors"><h4>Автор: {i[0]}\n</h4></div></a>'
    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
        <link rel="stylesheet" href="{url_for('static', filename='css/home.css')}">
    </head>
    <body>
        <header>
        <div>
           <div class="logo">
            <a href="home.html">
              <span class="use">NEWS</span>-<span class="web">NEWS</span>.ru
            </a>
           </div>


           <div class="top-menu">
             <ul>
                 <li><a class="clickMenu" href="/all-news">Все новости</a></li>
                 <li><a href="/all-author">Все авторы</a></li>
                 <li><a href="/add-news">Добавить новость</a></li>
             </ul>
           </div>


           <div class="block-top-auth">
             <p><a href="/login">Вход</a></p>
             <p><a href="/registration">Регистрация</a></p>
           </div>

        </header>

        <br>
        <h1 style="text-align: center;">ALL AUTHOR</h1>
        <br>
        <hr>
        <div>
        
        {news_block}

    </body>
    </html>"""

    return html


@app.route('/add-news', methods=['POST', 'GET'])
def add_news_func():
    if request.method == 'POST':
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        user = cursor.execute(f"SELECT * FROM Users WHERE name=?", (request.form.get('login'), )).fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        if user == None:
            return 'пользователя не существует'

        print(request.form.get('login'))  # достаем логин, который ввел пользователь
        print(request.form.get('content'))  # после достаем пароль

        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO news (name, content) VALUES (?, ?)',
                       (request.form.get('login'), request.form.get('content')))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(f"/all-news/{request.form.get('login')}")
    else:
        return render_template('add_news.html')


@app.route('/shop-list')
def shop_list_func():
    items = ['товар 1', 'товар 2', 'товар 3']
    return render_template('shop_list.html', items=items)



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="127.0.0.1", port=80)
    # Устанавливаем соединение с базой данных
