from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from . import db


class Enterprise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    users = db.relationship('User', backref='enterprise', lazy=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin'), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tickets = db.relationship('Ticket', backref='creator', lazy=True)
    messages = db.relationship('Message', backref='author', lazy=True)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.Text)
    status = db.Column(db.Enum('open', 'closed', 'pending'), default='open')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='ticket', lazy=True)
    participants = db.relationship('TicketUser', backref='ticket', lazy=True)


class TicketUser(db.Model):
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    role = db.Column(db.String(50))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='ticket_links')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    prediction = db.relationship('Prediction', uselist=False, backref='message')
    user = db.relationship('User', backref='messages_sent', lazy=True)



class ModelVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version_tag = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    accuracy = db.Column(db.Float)
    trained_on = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=False)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), unique=True)
    sentiment = db.Column(db.Enum('positive', 'neutral', 'negative'))
    confidence = db.Column(db.Float)
    model_version_id = db.Column(db.Integer, db.ForeignKey('model_version.id'))
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)
    model_version = db.relationship('ModelVersion', backref='predictions')


class RetrainingLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_version_id = db.Column(db.Integer, db.ForeignKey('model_version.id'))
    triggered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    log = db.Column(db.Text)
    status = db.Column(db.Enum('success', 'failed', 'pending'), default='pending')
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)


class MonitoringMetric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_version_id = db.Column(db.Integer, db.ForeignKey('model_version.id'))
    metric_name = db.Column(db.String(255))
    value = db.Column(db.Float)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)


class ApiAccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    endpoint = db.Column(db.String(255))
    method = db.Column(db.String(10))
    status_code = db.Column(db.Integer)
    auth_result = db.Column(db.Enum('success', 'fail'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class IncidentLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reported_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.Text)
    error_type = db.Column(db.String(255))
    status = db.Column(db.Enum('open', 'resolved'), default='open')
    resolution_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TestRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run_date = db.Column(db.DateTime, default=datetime.utcnow)
    result = db.Column(db.Enum('pass', 'fail'))
    triggered_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_cases = db.relationship('TestCase', backref='test_run', lazy=True)


class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_run_id = db.Column(db.Integer, db.ForeignKey('test_run.id'))
    name = db.Column(db.String(255))
    result = db.Column(db.Enum('pass', 'fail'))
    details = db.Column(db.Text)
