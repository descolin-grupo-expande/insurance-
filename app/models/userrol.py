from app.extensions import db

class UserRol(db.Model):
    """Docstring for UserRol. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    scope_country = db.Column(db.Integer)
    scope_sponsor = db.Column(db.Integer)
    scope_product = db.Column(db.Integer)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'UserRol({})'.format(self.id)
