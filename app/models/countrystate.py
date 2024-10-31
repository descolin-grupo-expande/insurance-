from app.extensions import db

class CountryState(db.Model):
    SDS_ZONES_BY_STATE = 'SDS_ZONES_BY_STATE'

    """Docstring for CountryState. """

    __tablename__ = 'state'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(50), nullable=False)
    country = db.Column(db.Integer, db.ForeignKey('country.id'))
    latitude = db.Column(db.Float(precision=53))
    longitude = db.Column(db.Float(precision=53))
    code_equivalence = db.Column(db.Integer)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'CountryState({})'.format(self.id)
