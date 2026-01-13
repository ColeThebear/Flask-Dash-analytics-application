from flask import Flask, redirect, render_template, request
from flask_login import login_user, logout_user, login_required, LoginManager
from models import User, db
from flask_bcrypt import Bcrypt
import dash

# 1. Initialize the Flask server
server = Flask(__name__)

# 2. (Optional) Initialize Dash if you are using it
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# 3. Initialize extensions (ensure 'bcrypt' is also defined)
bcrypt = Bcrypt(server)

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