from app.extensions import db
from datetime import datetime
from app.utils import check_full_token,gen_token

class User(db.Model):

    """Docstring for User. """

    __tablename__ = 'user_'

    STATUS_ACTIVE = 1
    STATUS_HIDDEN = 0


    APPLIES_DOUBLE_AUTHENTICATION_FACTOR = 1  # 1: aplica, 0: no aplica.

    #Password Status
    USER_PASSWORD_VALID=1
    USER_CHANGE_PASSWORD_FIRST_LOGIN=2
    USER_CHANGE_PASSORD_90_DIAS = 3
    USER_PASSWORD_RECOVERY = 4
    
    # Usuarios internos SC Asistencias
    # Teledoctor doctor y gastos medicos
    STATUS_DISABLED = 0
    STATUS_OFFLINE = 1    
    STATUS_ONLINE = 2
    STATUS_BUSY = 3
    STATUS_AWAY = 4
    STATUS_OFFLINE_AVAILABLE = 10

    USER_TYPE_CLIENT = 1
    USER_TYPE_PROVIDER = 2
    USER_TYPE_INTERNAL = 3
    USER_TYPE_TELEDOCTOR_CLIENT = 4
    USER_TYPE_TELEDOCTOR_DOCTOR = 5
    USER_TYPE_ASSISTANCE_PROVIDER = 6
    USER_TYPE_INSURANCE_EXT = 7
    USER_TYPE_MEDICAL_EXPENSES = 9
    USER_TYPE_SDS = 10


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #
    # remove unique email
    #
    email = db.Column(db.Unicode(255), nullable=False, index=True)
    name = db.Column(db.Unicode(128), nullable=False)
    # System username or bank ID
    #
    # remove unique username 
    #
    username = db.Column(db.Unicode(128), nullable=False)
    token = db.Column(db.Unicode(400))
    password_hash = db.Column(db.Unicode(128), nullable=False)
    ui_language = db.Column(db.Unicode(2))
    fcm_token = db.Column(db.Unicode(400))
    login_time = db.Column(db.DateTime)
    # Time of last user activity (any access to api)
    active_time = db.Column(db.DateTime)
    scope_country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    login_failed_amount = db.Column(db.Integer)
    applies_double_authentication_factor = db.Column(db.SmallInteger, default=0)
    secret = db.Column(db.Unicode(255))
    updated_time = db.Column(
        db.DateTime, nullable=False, onupdate=datetime.utcnow,
        default=datetime.utcnow
    )
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token_recovery_pasword = db.Column(db.Unicode(128), nullable=True)
    last_assigned_job = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger, default=1)
    password_change_status = db.Column(db.Integer)
    #roles = db.relationship('Role', secondary='user_rol')
    #scope_country = db.relationship('Country', foreign_keys = "[User.scope_country_id]")
    #country = db.relationship('Country', foreign_keys = "[User.country_id]")
    last_password_change = db.Column(db.DateTime)
    #twoFactorToken = db.relationship('TwoFactorToken', lazy = 'subquery')

    last_assigned_job = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger, default=1)

    # assistance sale update
    pin = db.Column(db.Unicode(50))
    national_id = db.Column(db.Unicode(50))
    phone_number = db.Column(db.Unicode(20))
    campaign_id = db.Column(db.Integer)
    first_name = db.Column(db.Unicode(64))
    last_name = db.Column(db.Unicode(64))

    # assistance providers update
    user_type = db.Column(db.Integer) 
    # cliente = 1
    # proveedor = 2
    # usuario_interno = 3
    # cliente teledoctor = 4
    # doctor teledoctor = 5
    photo = db.Column(db.Unicode(255))
    

    connection_status = db.Column(db.SmallInteger, default=STATUS_OFFLINE)
    site_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_site.id'))
    odontoprev_code = db.Column(db.Integer)

    @staticmethod
    def is_full_token(full_token):
        return check_full_token(full_token)

    @staticmethod
    def split_full_token(full_token):
        user_id, token = full_token.split('.', 1)
        user_id = int(user_id)
        return user_id, token

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'User({})'.format(self.id)

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
    
    def get_projection_auth(self):
        """TODO: Docstring for get_projection_auth.
        :returns: Usernae

        """
        return '{}'.format(self)