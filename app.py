from flask import Flask, redirect, jsonify
from flask_login import login_user, logout_user, login_required, LoginManager
from flask_bcrypt import Bcrypt
from config import DevelopmentConfig, TestingConfig, ProductionConfig, Config
from models import User, db
from auth import auth_bp
from dashboard import dashboard_bp, create_dashboard
import requests
from flask import render_template, request
import os

# Initialize Flask
server = Flask(__name__)

env = os.getenv("FLASK_ENV", "development")
if env == "production":
    server.config.from_object(ProductionConfig)
elif env == "testing":
    server.config.from_object(TestingConfig)
else:
    server.config.from_object(DevelopmentConfig)

# Initialize extensions
server.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(server)
bcrypt = Bcrypt(server)
login_manager = LoginManager(server)
login_manager.login_view = 'auth.login'

server.register_blueprint(auth_bp)
server.register_blueprint(dashboard_bp)

with server.app_context():
    db.create_all()

# Create tables
with server.app_context():
    db.create_all()

# User model
with server.app_context():
    db.create_all()

# User loader
@server.route('/')
def home():
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@server.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "User already exists."
        user = User(username=username, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect('/dashboard/')
        return "Invalid credentials."
    return render_template('login.html')

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@server.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "version": Config.APP_VERSION,
        "environment": Config.ENVIRONMENT,
        "commit": Config.get_git_commit()
    })

# Initialize Dash
dash_app = create_dashboard(server)

@server.route('/dashboard/')
@login_required
def protect_dashboard():
    # This route protects the Dash app mounted at /dashboard/
    return server.send_static_file('index.html')  # or just pass if Dash handles layout

if __name__ == '__main__':
    server.run(debug=True)