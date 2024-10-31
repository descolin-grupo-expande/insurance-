from app.extensions import db 

class UserSaleRelation(db.Model):
    """Docstring for UserSaleRelation. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_.id'), nullable=False)
    sale_id = db.Column(db.Integer, db.ForeignKey('assistance_sale.id'), nullable=False)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'UserSaleRelation({})'.format(self.id)
        