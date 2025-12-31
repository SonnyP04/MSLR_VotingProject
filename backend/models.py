from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import UniqueConstraint

db = SQLAlchemy() #in-built declarative base

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique = True, nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    scc = db.Column(db.String(10), unique=True, nullable=False)

class SccCodes(db.Model):
    __tablename__ = 'scc_codes'
    id = db.Column(db.Integer, primary_key=True)
    scc = db.Column(db.String(10), unique=True, nullable = False)
    usage = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Referendums(db.Model):
    __tablename__ = 'referendums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class ReferendumOptions(db.Model):
    __tablename__ = 'referendum_options'
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(255), nullable=False)
    referendum_id = db.Column(db.Integer, db.ForeignKey('referendums.id'))
    vote_count = db.Column(db.Integer, default=0)

class Votes(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('referendum_options.id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    referendum_id = db.Column(db.Integer, db.ForeignKey('referendums.id'))

    __table_args__ = (
        UniqueConstraint('user_id', 'option_id'),
    )




