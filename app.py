# Импорт необходимых библиотек
from flask import Flask, render_template, request, redirect
import psycopg2

# Создание объекта app, который и будет нашим приложением
app=Flask(__name__)

# Создание декоратора который зарегистрирует декорируемую функцию как маршрут
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '' or password == '':
                return 'Ошибка, заполните пустые поля'

            # Делаем SELECT запрос к базе данных, испоьзуя обычный SQL-синтаксис
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            # Извлекает все строки результата запроса
            records = list(cursor.fetchall())
            if not records:
                return 'Ошибка, данные введены неверно'

            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

# get чтения данных с сайта, post отправка данных на сайт
@app.route('/registration/', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == '' or login == '' or password == '':
            return 'Ошибка, заполните пустые поля'

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html')


# Создаем соединение с нашей базой, где  дополнительными параметрами являются: имя базы данных, имя пользователя, пароль, адрес хоста, номер порта
conn = psycopg2.connect(database="service",
                        user="postgres",
                        password="2258",
                        host="localhost",
                        port="5432")

# Создаем курсор - это спец объект, который делает запросы и получает их результаты
cursor = conn.cursor()

if __name__=="__main__":
    app.run()
