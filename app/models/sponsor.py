from app.extensions import db

class Sponsor(db.Model):
    """Docstring for Sponsor. """

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column(db.Unicode(50))
    sap_code = db.Column(db.Unicode(20))
    whatsapp = db.Column(db.Integer) 
    status = db.Column(db.SmallInteger, default=1)
    emails_manual_welcome_kit = db.Column(db.Text)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'Sponsor({})'.format(self.id)
