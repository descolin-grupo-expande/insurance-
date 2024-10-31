from app.extensions import db
from app import models as m

class CarBrand(db.Model):
    """Docstring for CarBrand.
        status
            0=Hidden
            1=Active
    """

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    priority = db.Column(db.Integer)
    attachment_id = db.Column(db.Integer, db.ForeignKey('attachment.id'))
    status = db.Column(db.SmallInteger, default=1)
    visible_ss = db.Column(db.SmallInteger, default=0)

    attachment = db.relationship(m.Attachment)


    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'CarBrand({})'.format(self.id)