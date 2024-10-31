from app.extensions import db
from datetime import datetime
from app.config import config
from app.utils.functions import check_full_token, gen_token

class AssistanceProvider(db.Model):

    """Docstring for AssistanceProvider.
        status:
            0: Hidden
            1: Active
            2: Emergency
            3: Pending
            4: Inactive
    """
    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1
    STATUS_EMERGENCY = 2
    STATUS_PENDING = 3
    STATUS_INACTIVE = 4

    NETWORK_TYPE_MEDICAL = 1
    NETWORK_TYPE_GENERAL = 2
    NETWORK_TYPE_DENTAL = 3
    NETWORK_TYPE_TELEDOCTOR = 4
    NETWORK_TYPE_ADMINISTRATIVE_SERVICES = 5

    PAYMENT_TYPE_CASH = 0
    PAYMENT_TYPE_CREDIT = 1

    ACCOUNT_TYPE_CHECKING_ACCOUNT = 0
    ACCOUNT_TYPE_SAVINGS_ACCOUNT = 1

    RFC_VALID = "Y"
    SELF_BILLING = "Y"

    IS_EXCLUDED = 1
    IS_NOT_EXCLUDED = 0

    #internalCompany values
    IC_ASI = 1
    IC_CUENTAME = 2

    # OG assistance providers
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(50))
    name = db.Column(db.Unicode(150), nullable=False)
    sap_code = db.Column(db.Unicode(20))
    priority = db.Column(db.Integer, nullable=False, default=1)
    latitude = db.Column(db.Float(precision=53))
    longitude = db.Column(db.Float(precision=53))
    service_area = db.Column(db.Float)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    contact_name = db.Column(db.Unicode(150))
    contact_phones = db.Column(db.Unicode(200))
    address = db.Column(db.Unicode(255))
    rating = db.Column(db.Float, default=0)
    quantity = db.Column(db.Integer, default=0)
    date_hire = db.Column(db.Date)
    status = db.Column(db.Integer, default=1)
    updated_time = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    government_id = db.Column(db.Unicode(50))
    legal_name = db.Column(db.Unicode(150))
    payment_name = db.Column(db.Unicode(150))
    billing_name = db.Column(db.Unicode(150))
    bank_account_name = db.Column(db.Unicode(150))
    bank_account_number = db.Column(db.Unicode(150))
    bank_account_type = db.Column(db.Integer)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    payment_type = db.Column(db.Integer)
    credit_days = db.Column(db.Integer)
    company_sap_db = db.Column(db.Unicode(100))
    contact_emails = db.Column(db.Unicode(300))
    bill_emails = db.Column(db.Unicode(300))
    coverage_area = db.Column(db.Unicode(400))
    state = db.Column(db.Unicode(100))
    city = db.Column(db.Unicode(100))
    district = db.Column(db.Unicode(100))
    observation = db.Column(db.Unicode(400))
    attention_time = db.Column(db.Unicode(200))
    cabin_name = db.Column(db.Unicode(100))
    phones_cabin = db.Column(db.Unicode(450))
    cabin_emails = db.Column(db.Unicode(400))
    phones_accounting = db.Column(db.Unicode(400))
    phones_web = db.Column(db.Unicode(400))
    equivalence_id = db.Column(db.Integer)
    # internal company
    internal_company = db.Column(db.Integer)
    provider_key = db.Column(db.Unicode(45), unique=True)
    billing_site = db.Column(db.Unicode(100))
    swift = db.Column(db.Unicode(100))
    cabin_visible = db.Column(db.Float)

    apply_retention_resico = db.Column(db.Boolean)
    retention_resico = db.Column(db.Float, default=1.25)

    rfc = db.Column(db.Unicode(255))
    tax_regime = db.Column(db.Unicode(255))
    base_url = db.Column(db.Unicode(255))
    _billing_token = db.Column("billing_token", db.Unicode(500))
    _billing_identifier = db.Column("billing_identifier", db.Unicode(500))
    network_type = db.Column(db.Integer)

    exclude_lock_date = db.Column(db.Integer, default=IS_NOT_EXCLUDED)

    country = db.relationship('Country', lazy='subquery')
    currency = db.relationship('Currency', lazy='subquery')
    services = db.relationship('AssistanceProviderService', lazy='subquery')
    

    billing_token = db.column_property(db.
            cast(
                db.func.aes_decrypt(
                    db.func.unhex(_billing_token), db.func.unhex(
                        db.func.sha2(config.WS_PRIVATE_KEY_MORFEO, 512))
                ),
                db.CHAR(255)
            ))

    
    billing_identifier = db.column_property(db.
            cast(
                db.func.aes_decrypt(
                    db.func.unhex(_billing_identifier), db.func.unhex(
                        db.func.sha2(config.WS_PRIVATE_KEY_MORFEO, 512))
                ),
                db.CHAR(255)
            ))



    @staticmethod
    def is_full_token(full_token):
        return check_full_token(full_token)

    @staticmethod
    def split_full_token(full_token):
        provider_id, token = full_token.split('.', 1)
        provider_id = int(provider_id)
        return provider_id, token

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceProvider({})'.format(self.id)

    def update_token(self):
        """TODO: Docstring for update_token.
        :returns: TODO

        """
        self.token = gen_token()

    def get_full_token(self):
        """TODO: Docstring for get_full_token.
        :returns: TODO

        """
        return '{}.{}'.format(self.id, self.token)

    # @hybrid_property
    # def users(self):
    #     return [
    #         user_provider.user
    #         for user_provider in (
    #             g.s()
    #                 .query(AssistanceProviderUser)
    #                 .filter(
    #                     AssistanceProviderUser.assistance_provider_id == self.id
    #                 ).all()
    #         )
    #     ]


# @event.listens_for(AssistanceProvider.billing_token, "set")
# def set_billing_token(target, value, oldvalue, initiator):

#     target._billing_token = db.func.hex(db.func.aes_encrypt(
#         value, db.func.unhex(db.func.sha2(config.WS_PRIVATE_KEY_MORFEO, 512))
#     ))


# @event.listens_for(AssistanceProvider.billing_identifier, "set")
# def set_billing_identifier(target, value, oldvalue, initiator):

#     target._billing_identifier = db.func.hex(db.func.aes_encrypt(
#         value, db.func.unhex(db.func.sha2(config.WS_PRIVATE_KEY_MORFEO, 512))
#     ))