from app.extensions import db
from datetime import datetime

class TableUpdate(db.Model):

    """Docstring for Update. """

    UPDATE_USER = 1
    UPDATE_MEMBER = 2
    UPDATE_ASSISTANCE_CASE = 3
    UPDATE_ASSISTANCE_BILL = 4
    UPDATE_ASSISTANCE_PROVIDER = 5
    UPDATE_ASSISTANCE = 6
    UPDATE_ASSISTANCE_SALE = 7
    UPDATE_INSURANCE_TICKET = 8
    UPDATE_INSURANCE_SALE = 9
    UPDATE_INSURANCE_SALE_ACCOUNTING = 10
    UPDATE_ASSISTANCE_CLAIM = 11
    UPDATE_MEDICAL_CASE = 12
    UPDATE_MEDICAL_BILL = 13
    UPDATE_MEDICAL_PROVIDER = 14
    UPDATE_MEDICAL_PRODUCT = 15
    UPDATE_MEDICAL_SALE = 16
    UPDATE_MEDICAL_PROVIDER_LOCATION = 17
    UPDATE_MEDICAL_PLAN_SERVICE = 18
    UPDATE_QUESTION = 19
    UPDATE_MEDICAL_LOCATION = 20
    UPDATE_MEDICAL_PLAN = 21
    UPDATE_REPORT_ATTACHMENT = 22
    UPDATE_ASSISTANCE_BILL_PRICE_EXTRA = 23
    UPDATE_IMPORT_FILE = 24
    UPDATE_TELEDOCTOR_CONSULTATION = 25
    UPDATE_TELEDOCTOR_SALE = 26
    UPDATE_TELEDOCTOR_TICKET = 27
    UPDATE_MEDICAL_PHARMACY_PRODUCT_LOCATION = 28
    UPDATE_MEDICAL_PROVIDER_SERVICE = 29
    UPDATE_MEDICAL_PROVIDER_LABORATORY = 30
    UPDATE_MEDICAL_CONSULTATION = 31
    UPDATE_TELEDOCTOR_USER = 32
    UPDATE_ASSISTANCE_PAYMENT_REQUIREMENT = 33
    UPDATE_MEDICAL_PAYMENT_REQUIREMENT = 34
    UPDATE_CMPG_TEMPLATE = 35
    UPDATE_PROSPECTS_FILE = 36
    UPDATE_CMPG_CAMPAIGN = 37
    UPDATE_MEDICAL_PLAN_COVERAGE = 38
    UPDATE_MEDICAL_PLAN_EXCLUSION = 39
    UPDATE_MEDICAL_PLAN_WAITTIME = 40
    UPDATE_ASSITANCE_COVER_LETTER = 41
    UPDATE_SINISTER_CLAIM = 42
    UPDATE_ASSISTANCE_PLAN = 43
    UPDATE_ASSISTANCE_SERVICE = 44
    UPDATE_SDS_BENEFICIARY_CUSTOMER_EMAIL = 45
    UPDATE_SDS_BENEFICIARY_CUSTOMER_PHONE = 46
    UPDATE_CANCEL_SDS_PROCEDURE = 47
    UPDATE_USER_ASSIGNED_IN_PROCEDURE = 48
    UPDATE_DELETE_SDS_PROCEDURE = 49
    UPDATE_INS_CREATE_JSON = 50
    UPDATE_INS_PAY_JSON = 51

    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    user_updated_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.Unicode(100))
    update_date = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)
    update_ip = db.Column(db.Unicode(50))
    update_agent = db.Column(db.Unicode(500))
    value_old = db.Column(db.Text)
    value_new = db.Column(db.Text)

    user = db.relationship('User',
                        backref='TableUpdate',
                        primaryjoin='foreign(TableUpdate.user_id) == remote(User.id)')
