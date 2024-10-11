from flask import Flask, render_template, request, url_for, redirect

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
    users.append(
        User(login, password)
    )
    return redirect(url_for('index'))

@app.route('/user/<int:user_id>')
def get_user(user_id):
    return users[user_id].__dict__

@app.route('/user')
def get_users():
    return [i.__dict__ for i in users]

if __name__ == '__main__':
    app.run()