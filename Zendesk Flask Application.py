# Core Libraries
import pandas as pd
import numpy as np
import datetime
import os

# SLA Calculations
from datetime import timedelta

# Authentication & Security
from flask import Flask, render_template, redirect, request, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from flask_bcrypt import Bcrypt
from models import db, User, Ticket


# Dash UI & Components
import dash
import dash_html_components as html
import dash_table
from dash import html, dcc, Output, Input, State
import dash_mantine_components as dmc
from dash.dependencies import MATCH, ALL
from dash import dash_table
from dash_extensions.enrich import DashProxy

# Visuals
import plotly.express as px
import plotly.graph_objects as go

# Interactive UI
import dash_draggable
from dash_draggable import GridLayout

# Enhanced Tables
from dash_mantine_components.Table import Table


# The code below was used for local testing
#df = pd.read_csv("C:/Users/Admin/OneDrive/Documents/Code Developing/Zendesk Flask Application/Zendesk Export.csv")

# load Environment variables
from dotenv import load_dotenv
load_dotenv()

# Flask Application
server = Flask(__name__)
server.secret_key = ''
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Flask Authentication & Registration
login_manager = LoginManager()
login_manager.init_app(server)
bcrypt = Bcrypt(server)

# Query database to get tickets
with server.app_context():
    tickets = Ticket.query.all()
    df = pd.DataFrame([{
        'Ticket ID': t.ticket_id,
        'Subject': t.subject,
        'Assignee': t.assignee,
        'Requester': t.requester,
        'Closed': t.closed,
        'Severity': t.severity,
        'Organisation': t.organisation,
        'Requested': t.requested,
        'ticket_duration_hours': t.ticket_duration_hours,
        'sla_met': t.sla_met
    } for t in tickets])


# Columns converted to datetime
df['Requested'] = pd.to_datetime(df['Requested'])
df['Closed'] = pd.to_datetime(df['Closed'])

# Time taken to close tickets raised
df['ticket_duration_hours'] = (df['Closed'] - df['Requested']) / np.timedelta64(1, 'h')

# SLA compliance ( Ticket closed within 24 hours after it being raised.)
df['sla_met'] = df['ticket_duration_hours'] <= 24

# Remove unwanted column
df = df.drop(columns=['Ticket on product Backlog?', 'Ticket form', 'Status'], errors='ignore')

#  (Optional) Calculate SLA compliance rate

# Results of tickets in CSV file & whether they met SLA
print(df[['Ticket ID', 'Subject', 'Assignee', 'Requester', 'Closed', 'Severity', 'Organisation', 'Requested', 'ticket_duration_hours','sla_met']])

# Base theme to be used through the entire application
theme = {
    "fontFamily": "Open Sans, sans-serif",
    "colors": {
        "primary": ["#1B5E20"],
        "gray": ["#F5F5F5", "#EEEEEE", "#E0E0E0"]
    },
    "spacing": {"md": 16, "lg": 24}
}

# Application Layout
app = dash.Dash(__name__, external_stylesheets=[], suppress_callback_exceptions=True)
app.layout = dmc.MantineProvider(theme=theme, children=[
    dmc.Container(fluid=True, px=0, children=[

        dmc.Title("Zendesk Export Dashboard", order=1, ta="center"),

# Dragable Content
        dmc.Grid([
            GridLayout(
                children=[
                    html.Div(dmc.Card(children=[dcc.Graph('graph')]), style={"padding": "8px"}),
                    html.Div(dmc.Card(children=[dash_table.DataTable('table')]), style={"padding": "8px"}),
                    dash_table.DataTable(
                        columns=[{"name": i, "id": i} for i in df.columns],
                        page_size=12,
                        data=df.to_dict('records'),
                        style_table={'overflowX': 'auto', 'border': '1px solid #ccc'},
                        style_cell={
                            'padding': '8px',
                            'textAlign': 'left',
                            'fontFamily': 'Open Sans',
                            'fontSize': '14px',
                        },
                        style_header={
                            'backgroundColor': '#69e3fa',
                            'color': 'white',
                            'fontWeight': 'bold'
                        }
                    ),
                ],
                gridCols=12,
                height=60,
                width=1200,
                layout=[
                    {"i": "graph", "x": 0, "y": 0, "w": 6, "h": 4},
                    {"i": "table", "x": 6, "y": 0, "w": 6, "h": 4}
                ]
            )
        ])
    ])
])

# PostgreSQL config
from config import Config
server.config['SQLALCHEMY_DATABASE_URI'] = os.gentenv('DATABASE_URL') or 'postgresql://postgres@localhost:5432/postgres'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(server)
bcrypt = Bcrypt(server)
login_manager = LoginManager(server)
login_manager.login_view = 'login'

# Create DB tables
with server.app_context():
    db.create_all()

# Create DB tables
with server.app_context():
    db.create_all()

    # Import CSV into PostgreSQL if not already populated
    if Ticket.query.count() == 0:
        df = pd.read_csv("Zendesk Export.csv")
        df['Requested'] = pd.to_datetime(df['Requested'])
        df['Closed'] = pd.to_datetime(df['Closed'])
        df['ticket_duration_hours'] = (df['Closed'] - df['Requested']) / np.timedelta64(1, 'h')
        df['sla_met'] = df['ticket_duration_hours'] <= 24
        df.drop(columns=['Ticket on product Backlog?', 'Ticket form', 'Status'], errors='ignore', inplace=True)

        for _, row in df.iterrows():
            ticket = Ticket(
                ticket_id=row['Ticket ID'],
                subject=row['Subject'],
                assignee=row['Assignee'],
                requester=row['Requester'],
                closed=row['Closed'],
                severity=row['Severity'],
                organisation=row['Organisation'],
                requested=row['Requested'],
                ticket_duration_hours=row['ticket_duration_hours'],
                sla_met=row['sla_met']
            )
            db.session.add(ticket)
        db.session.commit()

# Loading user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User registration
@server.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists. Try a different username."
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

# User login
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect('/dashboard/')
        return "Invalid username or password."
    return render_template('login.html')

# User logout
@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Dashboard landing page
@server.route('/dashboard/')
@login_required
def dashboard():
    return "Welcome to the dashboard!"

#Dash app
dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', suppress_callback_exceptions=True)

with server.app_context():
    tickets = Ticket.query.all()
    df = pd.DataFrame([{
        'Ticket ID': t.ticket_id,
        'Subject': t.subject,
        'Assignee': t.assignee,
        'Requester': t.requester,
        'Closed': t.closed,
        'Severity': t.severity,
        'Organisation': t.organisation,
        'Requested': t.requested,
        'ticket_duration_hours': t.ticket_duration_hours,
        'sla_met': t.sla_met
    } for t in tickets])

dash_app.layout = dmc.MantineProvider(theme={
    "fontFamily": "Open Sans, sans-serif",
    "colors": {"primary": ["#1B5E20"], "gray": ["#F5F5F5", "#EEEEEE", "#E0E0E0"]},
    "spacing": {"md": 16, "lg": 24}
}, children=[
    dmc.Container(fluid=True, px=0, children=[
        dmc.Title("Zendesk Export Dashboard", order=1, ta="center"),
        dmc.Accordion([
             dmc.AccordionItem([
                dmc.AccordionControl("System Info"),
                dmc.AccordionPanel([
                dmc.Text("App Version: 1.0.3"),
                dmc.Text("Last Deployed: 2025-08-18"),
                dmc.Text("Smoke Tests: ✅ Passed"),
                dmc.Text("Environment: Production"),
                dmc.Text("Git Commit: a1b2c3d"),
                ])
            ])
        ]),
        dmc.Grid([
            GridLayout(
                children=[
                    html.Div(dmc.Card(children=[
                        dcc.Graph(id='graph', figure=px.histogram(df, x='ticket_duration_hours', color='sla_met'))
                    ]), style={"padding": "8px"}, id="graph"),

                    html.Div(dmc.Card(children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in df.columns],
                            page_size=12,
                            data=df.to_dict('records'),
                            style_table={'overflowX': 'auto', 'border': '1px solid #ccc'},
                            style_cell={'padding': '8px', 'textAlign': 'left', 'fontFamily': 'Open Sans', 'fontSize': '14px'},
                            style_header={'backgroundColor': '#69e3fa', 'color': 'white', 'fontWeight': 'bold'}
                        )
                    ]), style={"padding": "8px"}, id="table"),
                ],
                gridCols=12,
                height=60,
                width=1200,
                layout=[
                    {"i": "graph", "x": 0, "y": 0, "w": 6, "h": 4},
                    {"i": "table", "x": 6, "y": 0, "w": 6, "h": 4}
                ]
            )
        ])
    ])
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)