from app.extensions import db
from datetime import datetime

class AssistanceSaleDependent(db.Model):
    """Docstring for AssistanceSaleDependent.
    """

    STATUS_ACTIVE = 1
    STATUS_HIDDEN = 0

    SELF = 0
    SPOUSE = 1
    SON = 2
    DAUGHTER = 3
    PARTNER = 4
    FATHER = 5
    MOTHER = 6
    FATHER_IN_LAW = 7
    MOTHER_IN_LAW = 8
    OTHER = 9
    BROTHER = 10

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assistance_sale_id = db.Column(db.Integer, db.ForeignKey('assistance_sale.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'))
    certificate_code = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, nullable=False, default=STATUS_ACTIVE)
    updated_time = db.Column(db.
        DateTime, nullable=False, onupdate=datetime.utcnow,
        default=datetime.utcnow
    )
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    member = db.relationship('Member', lazy=True)
    assistance_sale = db.relationship('AssistanceSale', lazy=True)
    relationship = db.Column(db.SmallInteger)

