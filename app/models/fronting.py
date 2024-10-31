from app.extensions import db

class Fronting(db.Model):
    """Docstring for Fronting. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    logo_attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    name = db.Column(db.Unicode(50))
    img_path = db.Column(db.Unicode(50))
    retention = db.Column(db.Float)
    country = db.relationship('Country')

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'Fronting({})'.format(self.id)
