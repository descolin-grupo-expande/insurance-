from app.extensions import db

class Catalog(db.Model):
    """Docstring for Catalog. """

    id = db.Column(db.Integer, primary_key=True)
    grouper = db.Column(db.Unicode(45))
    code = db.Column("code_", db.Unicode(45))
    description_es = db.Column(db.Unicode(256))
    description_en = db.Column(db.Unicode(256))

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return '    ({})'.format(self.id)
        