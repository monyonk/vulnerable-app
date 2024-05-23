from flask import Flask, request, render_template, jsonify, redirect, url_for
import psycopg2
import hashlib
import subprocess
import jwt
import datetime


app = Flask(__name__)

# Database configuration
DB_HOST = '127.0.0.1'
DB_NAME = 'vulner'
DB_USER = 'postgres'
DB_PASS = 'password123'

# Secret key 
SECRET_KEY = 'secret123'

def init_db():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            address TEXT,
            phone TEXT,
            email TEXT,
            hobby TEXT
        )
    ''')
    
    sample_users = [
        ('admin', 'admin', 'jakarta', '1234567890', 'admin@example.com', 'admin_hobby'),
        ('user1', 'password1', 'surabaya', '0987654321', 'user1@example.com', 'user1_hobby'),
        ('user2', 'password2', 'semarang', '1122334455', 'user2@example.com', 'user2_hobby')
    ]
    
    for user in sample_users:
        hashed_password = hashlib.md5(user[1].encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (username, password, address, phone, email, hobby) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (user[0], hashed_password, user[2], user[3], user[4], user[5])
        )

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashed_password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        token = jwt.encode({
            'user_id': user[0],
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token, 'user_id': user[0]})
    else:
        return jsonify({'message': 'Login failed'}), 401


@app.route('/get_profile', methods=['GET'])
def get_profile():
    token = request.args.get('token')
    user_id = request.args.get('id')  

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, address, phone, email, hobby FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            return jsonify({
                'user_id': user[0],
                'username': user[1],
                'address': user[2],
                'phone': user[3],
                'email': user[4],
                'hobby': user[5]
            })
        else:
            return jsonify({'message': 'User not found'}), 404
    
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/search')
def search():
    query = request.args.get('query')
    results = f"<p>Search results for: {query}</p>"
    return render_template('index.html', results=results)

@app.route('/ping', methods=['POST'])
def ping():
    ip = request.form['ip']
    command = f"ping -c 4 {ip}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return render_template('index.html', ping_results=result.stdout)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()

    app.run(debug=True, port=8000)
    





