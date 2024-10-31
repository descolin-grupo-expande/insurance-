from app.extensions import db

class WebServiceLog(db.Model):
    """Docstring for CatalogEquivalence. """

    STATUS_OK = 1
    STATUS_ERROR = 0
    STATUS_CONFIRMATION_OK = 2
    STATUS_CONFIRMATION_ERROR = 3

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    name = db.Column(db.Unicode(45))
    from_ = db.Column(db.Unicode(45))
    to_ = db.Column(db.Unicode(45))
    request_ = db.Column(db.Text)
    response_ = db.Column(db.Text)
    datetime = db.Column("datetime_", db.DateTime)
    policy_number = db.Column(db.Unicode(100))
    transaction_number = db.Column(db.Unicode(100))
    status = db.Column(db.SmallInteger, default=STATUS_OK)
    description = db.Column(db.Unicode(500))
    consecutive = db.Column(db.Unicode(255))
    product_code = db.Column(db.Unicode(255))
    plan_id = db.Column(db.Unicode(255))
    claim_number = db.Column(db.Unicode(100))
    chubb_claim_number = db.Column(db.Unicode(100))
    transaction_time = db.Column(db.Float)
    date_effective = db.Column(db.DateTime)
    price = db.Column(db.Numeric)
    reference_number = db.Column(db.Integer)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'WebServiceLog({})'.format(self.id)        