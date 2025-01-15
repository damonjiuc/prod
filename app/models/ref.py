from sqlalchemy.orm import backref
from app.extensions import db


class Ref(db.Model):
    __tablename__ = 'ref'
    id = db.Column(db.Integer, primary_key=True)
    referer_card = db.Column(db.Integer, db.ForeignKey('users.card'), nullable=False)
    request = db.relationship('Users', backref=backref('users', uselist=False))
    referral_card = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Integer, nullable=False)