from app.extensions import db


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    order_num = db.Column(db.String(11), nullable=False)
    name = db.Column(db.String(128))
    amount = db.Column(db.Float)
    amount_type = db.Column(db.String(128))
    price = db.Column(db.Float)
