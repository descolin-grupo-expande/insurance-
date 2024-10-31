from app.extensions import db

class AssistanceProviderService(db.Model):

    """Docstring for AssistanceProviderService. """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('assistance_service.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('assistance_provider.id'))

