from app.extensions import db

class AssistanceProviderCoverageArea(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), index=True , nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), index=True , nullable=True)
    provider_coverage_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_coverage.id'), index=True , nullable=True)
    status = db.Column(db.Integer)
    
    provider_coverage = db.relationship('AssistanceProviderCoverage')    
    state = db.relationship('CountryState', lazy = 'noload')    
    district = db.relationship('StateDistrict', lazy = 'noload')    

    
    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceProviderCoverageArea({})'.format(self.id)

   