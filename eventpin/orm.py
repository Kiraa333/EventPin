from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Добавленные поля
    avatar_url = db.Column(db.String(200))  # URL аватара пользователя
    phone_number = db.Column(db.String(20))  # Номер телефона
    birth_date = db.Column(db.Date)         # Дата рождения
    
    events = db.relationship('Event', backref='author', lazy=True, cascade='all, delete-orphan')
    visited_events = db.relationship('VisitedEvent', backref='visitor', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visits = db.relationship('VisitedEvent', backref='event', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_event_date', 'date'),
        db.Index('idx_event_category', 'category'),
    )
    
    def __repr__(self):
        return f'<Event {self.title}>'

class VisitedEvent(db.Model):
    __tablename__ = 'visited_events'
    
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer)
    review = db.Column(db.Text)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    
    def __repr__(self):
        return f'<VisitedEvent {self.event_id} by User {self.user_id}>'