from dbsetup import db, app
from datetime import datetime, timedelta

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    product_name = db.Column(db.String(50), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)