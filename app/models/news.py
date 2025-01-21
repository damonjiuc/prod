from app.extensions import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(82), nullable=False)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)