from app.extensions import db

class AssistancePlan(db.Model):

    """Docstring for AssistancePlan. """

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    FAMILY = 1
    PERSONAL = 2

    IS_RETENTION_PLAN = 1
    IS_NOT_RETENTION_PLAN = 0  

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(50))
    assistance_id = db.Column(db.Integer, db.ForeignKey('assistance.id'))
    coverage_name = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    base_price = db.Column(db.Float)
    life_months = db.Column(db.Integer)
    status = db.Column(db.Integer)
    arrear_months = db.Column(db.Integer)
    active_months = db.Column(db.Integer)

    services = db.relationship('AssistanceService', secondary='assistance_plan_service')
    addons = db.relationship('AssistancePlanAddon')
    currency = db.relationship('Currency')
    product = db.relationship('Assistance')
    
    programmed_sms = db.Column(db.Unicode(140))
    email_info_id = db.Column(db.Integer, db.ForeignKey('email_info.id'))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))

    email_info = db.relationship('EmailInfo')
    facturacion = db.Column(db.Boolean)
    collaborator = db.Column(db.SmallInteger, nullable=False, default=0)
    url_collaborator = db.Column(db.Integer)
    chubb_sale = db.Column(db.SmallInteger, nullable=False, default=0)
    buca_plan = db.Column(db.SmallInteger, default=0)
    sinister_plan = db.Column(db.SmallInteger, default=0)
    buca_email_info_id = db.Column(db.Integer)
    is_retention_plan = db.Column(db.SmallInteger, default=0)
    is_retention_plan_assistance = db.Column(db.SmallInteger, default=0)
    renewal_expiration_date = db.Column(db.SmallInteger, default=0)
