from app.extensions import db
from datetime import datetime

class AssistanceSale(db.Model):
    """Docstring for AssistanceSale. """

    STATUS_ACTIVE = 1
    STATUS_DELAYED = 2
    STATUS_CANCELED = 3
    STATUS_RENEWAL = 4
    STATUS_ARREAR = 5
    STATUS_PENDING = 6

    BILLING_CYCLE_MONTHLY = 0
    BILLING_CYCLE_QUARTERLY = 1
    BILLING_CYCLE_BIANNUAL = 2
    BILLING_CYCLE_ANNUAL = 3

    ISSUER_VISA = 1
    ISSUER_MASTERCARD = 2
    ISSUER_AMERICAN_EXPRESS = 3

    PAYMENT_GATEWAY_BAC = 1
    PAYMENT_GATEWAY_PAYPAL = 2

    PAYMENT_TYPE_CREADIT_CARD = 1
    PAYMENT_TYPE_DEBIT_CARD = 2
    PAYMENT_TYPE_CHECKING_ACCOUNT = 3
    PAYMENT_TYPE_SAVINGS_ACCOUNT = 4
    PAYMENT_TYPE_SERVICE_INVOICE = 5
    PAYMENT_TYPE_CREDIT_INVOICE = 6
    PAYMENT_TYPE_PAYROLL = 7
    PAYMENT_TYPE_PAYPAL = 8

    # Channels
    APOLO11 = 'APOLO11'
    TELEDOCTOR = "TELEDOCTOR"
    TMK = "TMK"
    F2F = "F2F"
    BULK = "BULK"
    WEBSERVICE = "WEBSERVICE"
    VPS = 'VPS'
    CRM = 'CRM'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    address = db.Column(db.Unicode(255))
    salesman_id = db.Column(db.Integer, db.ForeignKey('user_.id'))
    notes = db.Column(db.Unicode(500))
    expiration_date = db.Column(db.Date)
    payment_name = db.Column(db.Unicode(150))
    category = db.Column(db.Unicode(30))
    assistance_plan_id = db.Column(db.Integer, db.ForeignKey('assistance_plan.id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    date_issued = db.Column(db.DateTime, default=datetime.now)
    date_effective = db.Column(db.DateTime)
    billing_cycle = db.Column(db.Integer)
    code = db.Column(db.Unicode(50))
    free_assistance_period = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False, default=STATUS_ACTIVE)
    date_canceled = db.Column(db.Date)
    cancellation_reason = db.Column(db.Unicode(100))
    cancellation_comment = db.Column(db.Unicode(500))
    renewal_date = db.Column(db.Date)
    canceled_by = db.Column(db.Integer,db.ForeignKey('user_.id'))
    modification_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    attachment_policy_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    attachment_pass_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    payment_notes = db.Column(db.Unicode(100))
    member_sale_classification = db.Column(db.Integer)
    sale_channel = db.Column(db.Unicode(50))
    # created_time = db.Column(db.DateTime, default=datetime.now)
    # updated_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    member = db.relationship('Member')
    plan = db.relationship('AssistancePlan')
    country = db.relationship('Country')
    salesman = db.relationship('User', foreign_keys=[salesman_id])
    assistance_sale_car = db.relationship(
        'AssistanceSaleCar',
        primaryjoin="AssistanceSaleCar.assistance_sale_id == AssistanceSale.id "
    )
    # payments = db.relationship(
    #     'AssistancePaymentRequirement',
    #     backref='assistance_sale',
    #     lazy=True
    # )

    # @hybrid_property
    # def pending(self):
    #     return [
    #         payment
    #         for payment in self.payments
    #         if payment.status == AssistancePaymentRequirement.STATUS_PENDING
    #     ]
