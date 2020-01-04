from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "logged_in" in session:
            return func(*args, **kwargs)
        else:
            flash("Authentication is required please log in")
            return redirect(url_for('login'))
    return wrapper


@app.route('/', methods = ["GET", "POST"])
def login():
    error = None
    status_code = 200
    if request.method == "POST":
        if request.form['username'] != app.config["USERNAME"] or request.form["password"] != app.config["USERNAME"]:
            error = "Invalied user credentials, Please try again"
            status_code = 400
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))

    return render_template('login.html', error=error), status_code


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cursor = g.db.execute("SELECT * FROM posts")
    posts = [dict(title = row[0], post= row[1]) for row in cursor.fetchall()]
    return render_template('main.html', posts = posts)


@app.route('/add', methods=["POST"])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required, please try again")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute("INSERT INTO posts VALUES (?, ?)", (title, post))
        flash("New post addes succesfully")
        g.db.commit()
        g.db.close()
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)