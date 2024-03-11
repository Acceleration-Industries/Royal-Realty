from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow
from .helpers import get_image 

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email 
        self.password = self.set_password(password) 

    def set_password(self, password):
        return generate_password_hash(password)

    def __repr__(self):
        return f"<User: {self.username}>"

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expenses = db.relationship('Expense', backref='property', lazy=True)
    incomes = db.relationship('Income', backref='property', lazy=True)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
