from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('registrations.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        event_name TEXT,
        email TEXT,
        department TEXT
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    full_name = request.form['full_name']
    event_name = request.form['event_name']
    email = request.form['email']
    department = request.form['department']

    conn = sqlite3.connect('registrations.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registrations (full_name, event_name, email, department) VALUES (?, ?, ?, ?)",
        (full_name, event_name, email, department)
    )
    conn.commit()
    conn.close()

    return render_template(
        'success.html',
        name=full_name,
        event=event_name,
        email=email,
        department=department
    )

@app.route('/records')
def records():
    conn = sqlite3.connect('registrations.db')
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, email, department, event_name FROM registrations")
    data = cursor.fetchall()
    conn.close()
    return render_template('records.html', data=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)