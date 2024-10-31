from app.extensions import db
from app.utils.functions import check_full_token, gen_token

class Member(db.Model):
    """Docstring for Member.
        status:
            0: Inactive
            1: Active
        
        member_classification:
            250: Colaborador-Sponsor
            60: TO GAS
            50: DISCAPACIDAD    
            30: VIP
            20: top offender
            10: black_list
        
	db.relationship_status
            1: Single
            2: Married
            3: Divorced
            4: Widowed
    """

    GENDER_FAMEAL = 0
    GENDER_MALE = 1

    db.RELATIONSHIP_SELF = 0
    db.RELATIONSHIP_SPOUSE = 1
    db.RELATIONSHIP_SON = 2
    db.RELATIONSHIP_DAUGHTER = 3
    db.RELATIONSHIP_PARTNER = 4
    db.RELATIONSHIP_FATHER = 5
    db.RELATIONSHIP_MOTHER = 6
    db.RELATIONSHIP_FATHER_IN_LAW = 7
    db.RELATIONSHIP_MOTHER_IN_LAW = 8
    db.RELATIONSHIP_OTHER = 9

    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.Unicode(500), index=True)
    first_name = db.Column("first_name", db.Unicode(500), nullable=False)
    middle_name = db.Column("middle_name", db.Unicode(500))
    last_name = db.Column("last_name", db.Unicode(500))
    last_name_2 = db.Column("last_name_2", db.Unicode(500))
    married_name = db.Column("married_name", db.Unicode(500))
    birthday = db.Column("birthday", db.Unicode(500))
    gender = db.Column("gender", db.Unicode(500))
    db.relationship_status = db.Column("db.relationship_status", db.Unicode(500))
    national_id = db.Column("national_id", db.Unicode(500), index=True)
    mobile = db.Column("mobile", db.Unicode(500), index=True)
    phone1 = db.Column("phone1", db.Unicode(500))
    phone2 = db.Column("phone2", db. Unicode(500))
    phone3 = db.Column("phone3", db.Unicode(500))
    email = db.Column("email", db.Unicode(500))
    member_comment = db.Column("member_comment", db.UnicodeText)
    member_classification = db.Column(db.Integer)
    country = db.Column(db.Integer, db.ForeignKey('country.id'))
    address = db.Column("address", db.Unicode(500))
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))
    state_district_id = db.Column(db.Integer, db.ForeignKey('district.id'))
    password = db.Column("password", db.Unicode(500))
    state = db.Column("state", db.Unicode(500))
    city = db.Column("city", db.Unicode(500))
    district = db.Column("district", db.Unicode(500))
    zip_code = db.Column("zip_code", db.Unicode(500))
    latitude = db.Column("latitude", db.Unicode(500))
    longitude = db.Column("longitude", db.Unicode(500))
    friends = db.Column("friends", db.Unicode(500))
    education = db.Column("education", db.UnicodeText)
    work = db.Column("work", db.UnicodeText)
    tax_number = db.Column("tax_number", db.Unicode(500))
    tax_name = db.Column("tax_name", db.Unicode(500))
    tax_address = db.Column("tax_address", db.Unicode(500))
    facebook_uid = db.Column("facebook_uid", db.Unicode(500))
    facebook_token = db.Column("facebook_token", db.Unicode(500))
    google_uid = db.Column("google_uid", db.Unicode(500))
    verified_person = db.Column(db.Boolean)
    verified_email = db.Column(db.Boolean)
    verified_mobile = db.Column(db.Boolean)
    verified_phone = db.Column(db.Boolean)
    verified_card = db.Column(db.Boolean)
    notes = db.Column("notes", db.Unicode(500))
    status = db.Column("status", db.Unicode(500))
    token = db.Column("token", db.Unicode(400))
    photo = db.Column("photo", db.Unicode(500))


    
    membercountry = db.relationship('Country')
    state_district = db.relationship('StateDistrict')

    @staticmethod
    def is_full_token(full_token):
        return check_full_token(full_token)

    @staticmethod
    def split_full_token(full_token):
        client_id, token = full_token.split('.', 1)
        client_id = int(client_id)
        return client_id, token

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'Member({})'.format(self.id)

    def update_token(self):
        """TODO: Docstring for update_token.
        :returns: TODO

        """
        self.facebook_token = gen_token()

    def get_full_token(self):
        """TODO: Docstring for get_full_token.
        :returns: TODO

        """
        return '{}.{}'.format(self.id, self.facebook_token)


