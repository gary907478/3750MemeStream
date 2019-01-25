from flask import Flask, session, redirect, url_for, escape, request, render_template, send_from_directory
import json
from functools import wraps
import sys
import hashlib
from scraper import scraper
from db import DB

app = Flask(__name__, template_folder="templates")
app.secret_key = 'yeetyeetskeetskeet'

db = DB()

memescraper = scraper(do_logging=False, db_connection=db)
memescraper.start()

def ensure_logged_in():
    def _ensure_logged_in(f):
        @wraps(f)
        def __ensure_logged_in(*args, **kwargs):
            # just do here everything what you need

            if not 'username' in session:
                return redirect(url_for("catch_route"));

            result = f(*args, **kwargs)

            return result
        return __ensure_logged_in
    return _ensure_logged_in

def ensure_not_logged_in(redirect_to):
    def _ensure_not_logged_in(f):
        @wraps(f)
        def __ensure_not_logged_in(*args, **kwargs):
            # just do here everything what you need

            if 'username' in session:
                return redirect(url_for(redirect_to))

            result = f(*args, **kwargs)

            return result
        return __ensure_not_logged_in
    return _ensure_not_logged_in

@app.route('/protected')
@ensure_logged_in()
def protected_page():
    return "This is a protected page. Congrats you logged in" + \
        """<form action="/logout" method="post"> <button type="submit">Log out</button> </form>"""

@app.route('/login', methods=['POST'])
def login():
    name = request.form['username'].encode('utf-8')
    passwordHash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()

    cursor = db.execute("SELECT A_USERNAME from ACCOUNT_INFO where A_USERNAME=%s AND A_PASSWORD=%s",
                   (name, passwordHash,))
    if (not cursor.fetchone()):
        return "Login details incorrect"
    else:
        session['username'] = name
        return redirect(url_for('user_account'))

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['username'].encode('utf-8')
    passwordHash = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
    email = request.form['email'].encode('utf-8')

    cursor = db.execute("SELECT A_USERNAME, A_EMAIL from ACCOUNT_INFO where A_USERNAME=%s OR A_EMAIL=%s",
                   (name, email))
    if (cursor.fetchone()):
        return "Username or email already taken"

    cursor.execute("""INSERT into ACCOUNT_INFO (A_USERNAME, A_PASSWORD, A_EMAIL) VALUES (%s, %s, %s)""",
                   (name, passwordHash, email,))

    db.commit()

    return redirect(url_for('catch_route'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('catch_route'))

@app.route('/user_account.html')
@ensure_logged_in()
def user_account():
    cursor = db.execute("SELECT LINK FROM SCRAPED_MEMES");
    memes = [ (x[0], "mp4" in x[0]) for x in cursor ]
    return render_template('/user_account.html', memes=memes, session_user_name=session['username'])

@app.route('/')
@ensure_not_logged_in('user_account')
def log_in_page():
    return render_template('/main.html', session_user_name='test')

@app.route('/', defaults={"path": "main.html"})
@app.route('/<path:path>')
def catch_route(path):

    if (path.split('.')[-1] == "html"):
        return render_template(path, session_user_name="test")
    else:
        return send_from_directory("static", path)
