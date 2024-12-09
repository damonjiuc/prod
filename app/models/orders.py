from ..extensions import db


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(64))
    order_num = db.Column(db.String(11), nullable=False)
    order_date = db.Column(db.Date)
    shipment_date = db.Column(db.Date)
    payment_date = db.Column(db.Date)
    bonus = db.Column(db.Integer)
    customer_name = db.Column(db.String(64))
    order_sum = db.Column(db.Float)
    card_num = db.Column(db.Integer)
    card_was_given = db.Column(db.Date)
    address = db.Column(db.String(128))
    shop = db.Column(db.String(128))
    bonus_paid = db.Column(db.Integer)