from app.extensions import db

class Country(db.Model):
    """Docstring for Country.

    """
    country_phone_code = [
        {"country_id": 1, "phone_code": "502"},
        {"country_id": 4, "phone_code": "503"},
        {"country_id": 3, "phone_code": "504"},
        {"country_id": 5, "phone_code": "505"},
        {"country_id": 2, "phone_code": "506"},
        {"country_id": 7, "phone_code": "507"},
        {"country_id": 8, "phone_code": "52"},
        {"country_id": 9, "phone_code": "1"},
        {"country_id": 10, "phone_code": "1868"},
        {"country_id": 12, "phone_code": "595"}
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(50), nullable=False)
    locale = db.Column(db.String(5))
    timezone = db.Column(db.Integer)
    state_text = db.Column(db.String(20))
    state_district_text = db.Column(db.Unicode(20))
    tax_number = db.Column(db.String(20))
    tax_text = db.Column(db.String(20))
    national_id_text = db.Column(db.String(20))
    sap_code = db.Column(db.Unicode(20))
    currency_code = db.Column(db.Unicode(10))
    currency_symbol = db.Column(db.Unicode(10))
    assistance_phone = db.Column(db.Unicode(25))
    bill_email_info_id = db.Column(db.Integer)
    iso3166_1 = db.Column(db.String(2),nullable=True)
    s6_equivalence_code = db.Column(db.String(10))
    sms_client = db.Column(db.String(20))
    states = db.relationship('CountryState', primaryjoin="CountryState.country == Country.id")

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'Country({})'.format(self.id)
