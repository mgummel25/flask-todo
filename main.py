from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

app = Flask(__name__)
app.secret_key = b'Rd\x0fGK\xae\x91\xc5\x10\xe0\xbfX\xa2\xec&\xa9\x85tpe\x01\xa2\xcaC'


@app.route('/all')
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        task = Task(name=request.form['task'])
        task.save()

        return redirect(url_for('all_tasks'))

    else:
        return render_template('create.jinja2')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user = User.select().where(User.name == request.form['name']).get()

            if user and pbkdf2_sha256.verify(request.form['password'], user.password):
                print("this was hit")
                session['username'] = request.form['name']
                return redirect(url_for('all_tasks'))
        except Exception as e:
            error = "Incorrect username or password."
            return render_template('login.jinja2', error=error)

    else:
        return render_template('login.jinja2')

@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        pass        

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
