from flask_login import logout_user, login_required
from flask import Flask, redirect
from flask_bcrypt import Bcrypt
import dash

# 1. Initialize the Flask server
server = Flask(__name__)

# 2. (Optional) Initialize Dash if you are using it
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# 3. Initialize extensions (ensure 'bcrypt' is also defined)
bcrypt = Bcrypt(server)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')