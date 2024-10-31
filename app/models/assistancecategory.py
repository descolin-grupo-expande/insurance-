from app.extensions import db

class AssistanceCategory(db.Model):

    """Docstring for AssistanceCategory.
    status:
        0 = Hidden
        1 = Active
    """

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1

    VIAL = 1100

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(255))
    priority = db.Column(db.Integer, nullable=False, default=1)
    color = db.Column(db.Unicode(10))
    sap_code = db.Column(db.Unicode(20))
    status = db.Column(db.SmallInteger, nullable=False, default=1)
    image_url = db.Column(db.Unicode(150))
    code_equivalence = db.Column(db.Integer)
    buca_type = db.Column(db.Integer)
    odontoprev_code = db.Column(db.Integer)
