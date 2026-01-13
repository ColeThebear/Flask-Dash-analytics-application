from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Define Users for the database
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# Define Tickets for the database
class Ticket(db.Model):
    __tablename__ = 'tickets'

    ticket_id = db.Column(db.String(50), primary_key=True)
    subject = db.Column(db.String(255))
    assignee = db.Column(db.String(255))
    requester = db.Column(db.String(255))
    closed = db.Column(db.DateTime)
    severity = db.Column(db.String(50))
    organisation = db.Column(db.String(255))
    requested = db.Column(db.DateTime)
    ticket_duration_hours = db.Column(db.Float)
    sla_met = db.Column(db.Boolean)