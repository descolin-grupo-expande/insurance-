from app.extensions import db

class StateDistrict(db.Model):

    """Docstring for StateDistrict. """

    __tablename__ = 'district'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer)
    name = db.Column(db.Unicode(50), nullable=False)
    code_equivalence = db.Column(db.Integer)