from app.extensions import db
from datetime import datetime

class Assistance(db.Model):

    """Docstring for Assistance.
        status:
            0: Hidden
            1: Active
            2: Inactive
            3: Pending (default)
    """
    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2
    STATUS_PENDING = 3

    TYPE_ANTICIPATED = 1
    TYPE_OVERDUE = 0

    # CRM Retention types allowed
    # Retencion cancela venta antigua y se debe cobrar en S2
    CRM_CANCEL_RETENTION_PAYMENT = 10
    # Retencion cancela venta antigua y emite nueva venta a Apolo11 sin cobro
    CRM_CANCEL_RETENTION_NO_PAYMENT = 20
    # Retencion Upgrade no cancela venta antigua y emite nueva venta a Apolo11 sin cobro
    CRM_NO_CANCEL_RETENTION_NO_PAYMENT = 30

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assistance_code = db.Column(db.Unicode(20), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'))
    fronting_id = db.Column(db.Integer, db.ForeignKey('fronting.id'))
    name = db.Column(db.Unicode(50), nullable=False)
    description = db.Column(db.Unicode(500))
    service_number = db.Column(db.Unicode(50))
    status = db.Column(db.Integer, default=3)
    updated_time = db.Column(db.
        DateTime, nullable=False, onupdate=datetime.utcnow,
        default=datetime.utcnow
    )
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recurring_charge = db.Column(db.Boolean, nullable=False)
    charge_type = db.Column(db.Integer, nullable=False)
    crm_retention_type = db.Column(db.Integer)
    cabin_contact_phones = db.Column(db.Unicode(400), nullable=True)
    providers_cabin_contact_phones = db.Column(db.Unicode(400), nullable=True)
    country = db.relationship('Country')
    sponsor = db.relationship('Sponsor', lazy='select')
    fronting = db.relationship('Fronting')
