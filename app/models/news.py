from app.extensions import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(82), nullable=False)
    description = db.Column(db.String(320), nullable=False)
    img = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)