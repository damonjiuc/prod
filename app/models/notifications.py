from app.extensions import db


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    device_type = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    last_send = db.Column(db.Date, nullable=True)