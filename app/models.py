from app import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_replenish = db.Column(db.Boolean, nullable=False, default=True)
