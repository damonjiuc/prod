from datetime import datetime

from ..extensions import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.Integer, nullable=False)
    surname = db.Column(db.String(31))
    name = db.Column(db.String(31))
    secname = db.Column(db.String(31))
    email = db.Column(db.String(47))
    phone = db.Column(db.Integer)
    password = db.Column(db.String(255))
    active = db.Column(db.Integer, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    dateofreg = db.Column(db.DateTime, default=datetime.utcnow)
    lastauth = db.Column(db.DateTime)
    birthday = db.Column(db.Date)
    company = db.Column(db.String(47))
    city = db.Column(db.String(31))
    referer = db.Column(db.Integer)
    bankcard = db.Column(db.Integer)
    bankname = db.Column(db.String(31))
    cardholder = db.Column(db.String(31))
    avatar = db.Column(db.String(127))
    lvl = db.Column(db.Integer, nullable=False)
    moneytomln = db.Column(db.Float)
    totalmoney = db.Column(db.Float)
    apptoken = db.Column(db.String(255))
