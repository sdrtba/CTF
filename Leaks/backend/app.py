from flask import Flask, request, jsonify
import jwt
import datetime
import random
import sqlite3
import os

app = Flask(__name__)
SECRET = "cb89417f-4e45-4600-9b42-70941c488ade"
DB_PATH = "users.db"

NOTES = [
    "Really nice day!",
    "Good job!",
    "God is just a joke.",
    "Stay focused!",
    "You're doing great.",
    "Code like a hero.",
    "Trust your instincts.",
    "Never give up!",
    "More coffee, please.",
    "It's debug o'clock.",
    "Hack the planet.",
    "Keep your secrets safe.",
    "404 motivation not found.",
    "Exploit your potential.",
    "Break stuff, learn stuff.",
    "Trust no input.",
    "Reboot your mindset.",
    "This is fine 🔥.",
]


def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                note TEXT NOT NULL
            )
        """)
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (
            "admin",
            "super_secret_password_664432920",
            "flag{d0n7_l0s3_y0ur_k3y$}"
        ))
        conn.commit()
        conn.close()


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    note = random.choice(NOTES)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if c.fetchone():
        return jsonify({'error': 'User exists'}), 400

    c.execute("INSERT INTO users (username, password, note) VALUES (?, ?, ?)",
              (username, password, note))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registered'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['username']

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()

    if not row or row[0] != password:
        return jsonify({'error': 'Invalid credentials'}), 401


    token = jwt.encode(
        {
            'user_name': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET,
        algorithm='HS256'
    )
    return jsonify({'token': token})


@app.route('/api/profile', methods=['GET'])
def profile():
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer '):
        return jsonify({'error': 'Missing token'}), 401

    token = auth[7:]
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        username = data['user_name']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT note FROM users WHERE username = ?", (username,))
        row = c.fetchone()
        conn.close()

        if row:
            return jsonify({'user': username, 'note': row[0]})
        else:
            return jsonify({'error': 'User not found'}), 404

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 403


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)
