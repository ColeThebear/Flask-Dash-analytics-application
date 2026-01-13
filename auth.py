from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user, login_required
from models import User, db
from extensions import bcrypt
# from app import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            # Redirect to register page if user doesn't exist
            return redirect('/register')

        if bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect('/dashboard/')
        else:
            return "Invalid password"
        
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Username already exists"

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@auth_bp.route('/logout')

@login_required
def logout():
    logout_user()
    return redirect('/login')