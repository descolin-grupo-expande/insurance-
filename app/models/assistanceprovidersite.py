from app.extensions import db

class AssistanceProviderSite(db.Model):

    HIDDEN = 0
    ACTIVE = 1
    INACTIVE = 2
    DOWN = 3 
    PROCESS = 4

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    provider_id = db.Column(db.Integer, db.ForeignKey('assistance_provider.id'), index=True ,nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), index=True ,  nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), index=True , nullable=True)
    name = db.Column(db.Unicode(255), nullable=True)
    status = db.Column(db.Integer)
    iva = db.Column(db.Integer)
    equivalence_id = db.Column(db.Integer, unique=True)
    latitude = db.Column(db.DOUBLE)
    longitude = db.Column(db.DOUBLE)
    city = db.Column(db.Unicode(255), nullable=True)
    country_id = db.Column(db.Integer)
    address = db.Column(db.Unicode(255), nullable=True)
    cabin_name = db.Column(db.Unicode(100), nullable=True)
    cabin_emails = db.Column(db.Unicode(400), nullable=True)
    cabin_phones = db.Column(db.Unicode(400), nullable=True)
    attention_time = db.Column(db.Unicode(200), nullable=True)
    coordination_time = db.Column(db.Unicode(200), nullable=True)
    observation = db.Column(db.Text, nullable=True)
    apply_billing = db.Column(db.Boolean, default=True)



    provider = db.relationship('AssistanceProvider')    
    state = db.relationship('CountryState')    
    district = db.relationship('StateDistrict')    

    
    assistanceProviderCoverages = db.relationship('AssistanceProviderCoverage')
    
    
    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceProviderSite({})'.format(self.id)

   