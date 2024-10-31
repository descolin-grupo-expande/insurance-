from app.extensions import db

class AssistanceAppCase(db.Model):
    """Docstring for AssistanceCaseApp.

    """

    # STATUS_ASSIGNED = 1
    # STATUS_UNASSIGNED = 2
    
    STATUS_OPEN = 1
    STATUS_CLOSED = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assistance_case_id = db.Column(db.Integer, db.ForeignKey('assistance_case.id'))
    assistance_service_id = db.Column(db.Integer, db.ForeignKey('assistance_service.id'))
    latitude = db.Column(db.DOUBLE)
    longitude = db.Column(db.DOUBLE)
    status = db.Column(db.Integer, default=STATUS_OPEN)
    rating = db.Column(db.Integer)
    review = db.Column(db.Unicode(500))
    #provider_id = db.Column(db.Integer, ForeignKey('assistance_providers.id'))
    provider_user_id = db.Column(db.Integer, db.ForeignKey('user_.id'))

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceAppCase({})'.format(self.id)
