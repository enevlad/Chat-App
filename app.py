# app.py
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
socketio = SocketIO(app)
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    if 'username' in session:
        return redirect('/chat')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        session['username'] = username
        return redirect('/chat')
    return 'Invalid credentials, try again.'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            return 'User already exists.'
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    return render_template('chat.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# WebSocket events
@socketio.on('message')
def handle_message(msg):
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        new_message = Message(user_id=user.id, content=msg, timestamp=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()
        send({'username': username, 'message': msg}, broadcast=True)

if __name__ == '__main__':
    if not os.path.exists('chat.db'):
        with app.app_context():
        	db.create_all()
    socketio.run(app, debug=True)
