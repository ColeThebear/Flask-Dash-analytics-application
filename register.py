from flask import render_template, request, redirect
from flask import Flask
from flask_bcrypt import Bcrypt
from models import User , db
import dash

# 1. Initialize the Flask server
server = Flask(__name__)

# 2. (Optional) Initialize Dash if you are using it
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# 3. Initialize extensions (ensure 'bcrypt' is also defined)
bcrypt = Bcrypt(server)

@server.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            return "User already exists."
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')