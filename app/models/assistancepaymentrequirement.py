from app.extensions import db
from datetime import datetime

class AssistancePaymentRequirement(db.Model):
    """Docstring for AssistancePaymentRequirement.
        payments required for sales in assistance sales
    """
    STATUS_CANCELED = 0
    STATUS_PAYED = 1
    STATUS_PENDING = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assistance_sale_id = db.Column(db.Integer, db.ForeignKey('assistance_sale.id'))
    status = db.Column(db.Integer)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Numeric(precision=12, scale=2))
    charge_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    authorization_code = db.Column(db.Integer)
    comment = db.Column(db.Unicode(255))
    serial_number = db.Column(db.Integer)
    paid_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    report_amount = db.Column(db.Numeric(precision=12, scale=2))

    #assistance_sale = relationship('AssistanceSale', lazy=True)

    # @hybrid_property
    # def month(self):
    #     return self.charge_date.month