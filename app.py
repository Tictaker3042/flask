from flask import Flask, abort, render_template, request, url_for, redirect
import psycopg2
app = Flask(__name__)

class User:

    def __init__(self, login, password):
        self.login = login
        self.password = password


@app.route('/')
def index():
    return render_template('index.html')

users = []

@app.route('/user/create', methods=['POST'])
def create_user():
    login = request.form['login']
    password = request.form['password']
    connection = psycopg2.connect(database="users_application", user="administrator",
                                  password="root", host="localhost", port="5432")
    cursor = connection.cursor()

    cursor.execute('''INSERT INTO USERS(login, password)
    VALUES (%s, %s);''', (login, password))

    connection.commit()
    connection.close()
    cursor.close()

    return redirect(url_for('index'))


@app.route('/user/all')
@app.route('/user/<int:user_id>')
def get_user(user_id=None):
    connection = psycopg2.connect(database="users_application", user="administrator",
                                  password="root", host="localhost", port="5432")
    cursor = connection.cursor()

    if user_id is None:
        cursor.execute('''SELECT * FROM USERS''')
        users_data = cursor.fetchall()
        connection.close()
        cursor.close()


        return [User(i[0], i[1]).__dict__ for i in users_data]

    cursor.execute('''SELECT * FROM USERS WHERE user_order=%s''', [user_id])

    user_data = cursor.fetchall()

    connection.close()
    cursor.close()

    if user_data.__len__() == 0:
        return abort(404, f"User with id {user_id} not found")

    return User(user_data[0][0], user_data[0][1]).__dict__

@app.route('/user')
def get_users():
    return [i.__dict__ for i in users]

if __name__ == '__main__':
    app.run()