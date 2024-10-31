from app.extensions import db

class Bank(db.Model):
    """Docstring for Bank. """

    __tablename__ = 'bank'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column(db.Unicode(50))
    finances_auto = db.Column(db.Boolean)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'Bank({})'.format(self.id)
