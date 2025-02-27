from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)  # ETH address is 42 chars including '0x'
    xp_total = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quests_progress = db.relationship('QuestProgress', backref='user', lazy=True)

class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    xp_reward = db.Column(db.Integer, nullable=False)
    required_level = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    progress = db.relationship('QuestProgress', backref='quest', lazy=True)

class QuestProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quest.id'), nullable=False)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)