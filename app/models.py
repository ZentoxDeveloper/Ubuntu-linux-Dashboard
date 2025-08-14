from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='User')
    profile_image_url = db.Column(db.String(255), default='https://placehold.co/150x150')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    chat_messages = db.relationship('ChatMessage', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'Administrator'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'profile_image_url': self.profile_image_url,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'username': self.author.username,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'description': self.description,
            'ip_address': self.ip_address,
            'timestamp': self.timestamp.isoformat(),
            'username': self.user.username if self.user else 'System'
        }
    
    def __repr__(self):
        return f'<AuditLog {self.id}: {self.action}>'

class SystemMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    cpu_percent = db.Column(db.Float)
    memory_percent = db.Column(db.Float)
    disk_percent = db.Column(db.Float)
    network_bytes_sent = db.Column(db.BigInteger)
    network_bytes_recv = db.Column(db.BigInteger)
    load_average = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'cpu_percent': self.cpu_percent,
            'memory_percent': self.memory_percent,
            'disk_percent': self.disk_percent,
            'network_bytes_sent': self.network_bytes_sent,
            'network_bytes_recv': self.network_bytes_recv,
            'load_average': self.load_average
        }
    
    def __repr__(self):
        return f'<SystemMetrics {self.timestamp}>'

class ServiceStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False, unique=True)
    status = db.Column(db.String(20), nullable=False)  # active, inactive, failed
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    auto_start = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
            'status': self.status,
            'last_checked': self.last_checked.isoformat(),
            'auto_start': self.auto_start
        }
    
    def __repr__(self):
        return f'<ServiceStatus {self.service_name}: {self.status}>'
