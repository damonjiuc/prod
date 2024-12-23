from ..extensions import db


class Prizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(16), nullable=False)
    date = db.Column(db.Date)