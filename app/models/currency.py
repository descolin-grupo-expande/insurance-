from app.extensions import db

class Currency(db.Model):

    """Docstring for Assistance. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    currency_code = db.Column(db.Unicode(10))
    iso_code = db.Column(db.Unicode(3))
    symbol = db.Column(db.Unicode(1))

    country = db.relationship('Country')
