from app.extensions import db
from datetime import datetime

class AssistanceService(db.Model):
    """Docstring for AssistanceService.
    service_type:
        1 = Remote
        2 = Call
        3 = On-site
        4 = Programmed
    status:
        0 = Hidden
        1 = Active

    status_app:
        0 = Hidden
        1 = Active    
    
    app_required_delivery:
        0 = false
        1 = true
    """

    SERVICE_TYPE_REMOTE = 1
    SERVICE_TYPE_CALL = 2
    SERVICE_TYPE_ON_SITE = 3
    SERVICE_TYPE_PROGRAMMED = 4

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1

    STATUS_APP_HIDDEN = 0
    STATUS_APP_ACTIVE = 1

    APP_REQUIRED_DELIVERY = 1
    APP_NOT_REQUIRED_DELIVERY = 0
    APP_CALL_PHONE = 2
    APP_OPEN_TELEDOCTOR = 3

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(150))
    category_id = db.Column(db.Integer, db.ForeignKey('assistance_category.id'))
    description = db.Column(db.UnicodeText(500))
    updated_time = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    service_type = db.Column(db.Integer)
    expected_time = db.Column(db.Float)
    expected_time_customer = db.Column(db.Float)
    abbreviation = db.Column(db.Unicode(20))
    status = db.Column(db.SmallInteger, default=1)
    status_app = db.Column(db.SmallInteger, default=0)
    app_required_delivery = db.Column(db.SmallInteger, default=0)
    category = db.relationship('AssistanceCategory')
    image_url = db.Column(db.Unicode(150))

    # code_equivalence = db.Column(db.Integer)
    required_address = db.Column(db.SmallInteger, default=1)
    # send_information_geocercas = db.Column(db.SmallInteger, default=1)
    
    location = db.Column(db.Unicode(25))
    special_authorization = db.Column(db.Integer)
    pre_approbation = db.Column(db.Integer)
    notes = db.Column(db.UnicodeText(400))
    buca_service = db.Column(db.SmallInteger,  default=None)
    tooth_service = db.Column(db.SmallInteger,  default=None)
    sinister_service = db.Column(db.SmallInteger,  default=None)


    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceService({})'.format(self.id)
