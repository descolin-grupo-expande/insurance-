from app.extensions import db
from datetime import datetime

class Rol(db.Model):

    """Docstring for Rol. """

    MEDICAL_DOCTOR_ROLE = 19
    MEDICAL_OPERATOR_ROLE = 34   
    SDS_PROVIDER_ROLE = 1672
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(80), nullable=False, unique=True)
    updated_time = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow, default=datetime.utcnow)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'Rol({})'.format(self.name.encode('utf-8'))
