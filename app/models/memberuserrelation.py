from app.extensions import db

class MemberUserRelation(db.Model):
    """Docstring for MemberUserRelation. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_.id'), nullable=False)
    user = db.relationship('User', lazy='subquery')

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'MemberUserRelation({})'.format(self.id)
        