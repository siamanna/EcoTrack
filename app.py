from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key" 
DATABASE = 'data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()

        db.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT UNIQUE NOT NULL, 
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        name TEXT,
                        preferences TEXT)''')

        db.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        thread_type TEXT,
                        caption TEXT,
                        date DATE,
                        reply_to INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (reply_to) REFERENCES posts(id))''')
        db.commit()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    threads = db.execute("SELECT DISTINCT thread_type FROM posts").fetchall()
    return render_template('index.html', threads=threads, username=session['username'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        preferences = request.form['preferences']
        db = get_db()
        try:
            db.execute('INSERT INTO users (name, email, username, password, preferences) VALUES (?, ?, ?, ?, ?)',
                       (name, email, username, password, preferences))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists. Try another one."
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/thread/<thread_type>', methods=['GET', 'POST'])
def thread(thread_type):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    if request.method == 'POST':
        caption = request.form['caption']
        reply_to = request.form.get('reply_to', None)
        db.execute('INSERT INTO posts (user_id, thread_type, caption, date, reply_to) VALUES (?, ?, ?, ?, ?)',
                   (session['user_id'], thread_type, caption, datetime.now().date(), reply_to))
        db.commit()
    posts = db.execute('''SELECT posts.*, users.username 
                          FROM posts 
                          JOIN users ON posts.user_id = users.id 
                          WHERE posts.thread_type = ? 
                          ORDER BY posts.date DESC''', (thread_type,)).fetchall()
    return render_template('thread.html', posts=posts, thread_type=thread_type)

@app.route('/dailychallenges')
def daily_challenges():
    return render_template('dailychallenges.html')

@app.route('/weeklychallenges')
def weekly_challenges():
    return render_template('weeklychallenges.html')

@app.route('/monthlychallenges')
def monthly_challenges():
    return render_template('monthlychallenges.html')

@app.route('/yearlychallenges')
def yearly_challenges():
    return render_template('yearlychallenges.html')

@app.route('/sustainabilityjournal')
def sustainability_journal():
    return render_template('sustainabilityjournal.html')

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
