from app.extensions import db

class AssistancePlanAddon(db.Model):

    """Docstring for AssistancePlan. """

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    FAMILY = 1
    PERSONAL = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(50))
    assistance_plan_id = db.Column(db.Integer, db.ForeignKey('assistance_plan.id'))
    coverage_name = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    base_price = db.Column(db.Float)
    life_months = db.Column(db.Integer)
    status = db.Column(db.Integer)
    arrear_months = db.Column(db.Integer)
    active_months = db.Column(db.Integer)

    services = db.relationship('AssistanceService', secondary='assistance_plan_service')
    currency = db.relationship('Currency')
    plan = db.relationship('AssistancePlan')
    
    programmed_sms = db.Column(db.Unicode(140))
    email_info_id = db.Column(db.Integer, db.ForeignKey('email_info.id'))
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))

    email_info = db.relationship('EmailInfo')
    facturacion = db.Column(db.Boolean)
    collaborator = db.Column(db.SmallInteger, nullable=False, default=0)
    url_collaborator = db.Column(db.Integer)
    chubb_sale = db.Column(db.SmallInteger, nullable=False, default=0)
    buca_plan = db.Column(db.SmallInteger, default=0)