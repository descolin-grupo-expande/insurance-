from app.extensions import db
from datetime import datetime

class AssistancePrice(db.Model):

    """Docstring for AssistancePrice. """

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_coverage_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_coverage.id'), index=True )
    service_id = db.Column(db.Integer, db.ForeignKey('assistance_service.id'), index=True )
    provider_service_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_service.id'), index=True )
    hour_start=db.Column(db.Time)
    hour_end=db.Column(db.Time)
    note=db.Column(db.Unicode(500))
    price_small_vehicle=db.Column(db.Numeric(precision=12, scale=2))
    price_medium_vehicle=db.Column(db.Numeric(precision=12, scale=2))
    price_large_vehicle=db.Column(db.Numeric(precision=12, scale=2))
    price_extra_base_to_sinister=db.Column(db.Numeric(precision=12, scale=2))
    price_extra_sinister_to_destination=db.Column(db.Numeric(precision=12, scale=2))
    price_extra_extraction=db.Column(db.Numeric(precision=12, scale=2))
    price_weekday = db.Column(db.Numeric(precision=12, scale=2))
    price_weekend = db.Column(db.Numeric(precision=12, scale=2))
    price_holiday = db.Column(db.Numeric(precision=12, scale=2))
    price_extra = db.Column(db.Numeric(precision=12, scale=2))
    price_night = db.Column(db.Numeric(precision=12, scale=2))
    price_phone = db.Column(db.Numeric(precision=12, scale=2))
    price_presence = db.Column(db.Numeric(precision=12, scale=2))
    price_flag = db.Column(db.Numeric(precision=12, scale=2))
    price_cancellation = db.Column(db.Numeric(precision=12, scale=2))
    price_cancellation_flag = db.Column(db.Numeric(precision=12, scale=2))
    price_house = db.Column(db.Numeric(precision=12, scale=2))
    price_saturday = db.Column(db.Numeric(precision=12, scale=2))
    price_sunday = db.Column(db.Numeric(precision=12, scale=2))
    dead_percentage_local = db.Column(db.Numeric(precision=12, scale=2))
    dead_percentage = db.Column(db.Numeric(precision=12, scale=2))
    dead_percentage_kms = db.Column(db.Numeric(precision=12, scale=2))
    max_amount = db.Column(db.Numeric(precision=12, scale=2))
    is_fixed = db.Column(db.Integer)
    updated_time = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    copay = db.Column(db.Numeric(precision=12, scale=2))
    insurance_payment = db.Column(db.Numeric(precision=12, scale=2))
    status = db.Column(db.Integer, nullable=False, default=STATUS_ACTIVE)
    procesado_sc = db.Column(db.Boolean)


    assistanceService = db.relationship('AssistanceService', lazy = 'noload') 
    provider_coverage = db.relationship('AssistanceProviderCoverage', overlaps="assistancePrices", lazy='noload')
