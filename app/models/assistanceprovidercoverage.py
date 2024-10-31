from app.extensions import db
from app import models as m

class AssistanceProviderCoverage(db.Model):

    LOCAL = 1
    CARRETERO = 2
    ACTIVE = 1
    INACTIVE = 0

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    provider_site_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_site.id'), index=True , nullable=False)
    plane = db.Column(db.Integer)
    name = db.Column(db.Unicode(255), nullable=False)
    distance = db.Column(db.DOUBLE) # Para foraneos
    coverage_type = db.Column(db.SmallInteger) # 1 = LOCAL  |  2 = FORANEO/CARRETERO
    status = db.Column(db.Integer)


    assitanceProviderCoverageAreas = db.relationship('AssistanceProviderCoverageArea', overlaps="provider_coverage",  lazy = 'noload' )
    assistancePrices = db.relationship(m.AssistancePrice) 
    provider_site = db.relationship('AssistanceProviderSite', overlaps="assistanceProviderCoverages")

   
    
    
    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceProviderCoverage({})'.format(self.id)

   