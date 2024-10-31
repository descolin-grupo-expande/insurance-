from app.extensions import db

class CarModel(db.Model):
    """Docstring for CarModel.
        category
            1=Auto
            2=SUV
            3=Pickup
            4=Truck
            5=Motorcycle
            6=Panel
            7=Minibus
            8=Bus
        status
            0=Hidden
            1=Active
    """
    
    STATUS_HIDDEN = 0
    STATUS_ACTIVE = 1

    CATEGORY_AUTO = 1
    CATEGORY_SUV = 2
    CATEGORY_PICKUP = 3
    CATEGORY_TRUCK = 4
    CATEGORY_MOTORCYCLE = 5
    CATEGORY_PANEL = 6
    CATEGORY_MINIBUS = 7
    CATEGORY_BUS = 8
    CATEGORY_OTHER = 9
    CATEGORY_RENT = 10
    CATEGORY_AMBULANCE = 11
    CATEGORY_BUS_TRANS = 12
    CATEGORY_HEAD = 13
    CATEGORY_LIGHT_TRUCK = 14
    CATEGORY_HEAVY_TRUCK = 15
    CATEGORY_QUADRIMOTO = 16
    CATEGORY_MICROBUS = 17
    CATEGORY_MICROBUS_TRANS = 18
    CATEGORY_TRAILER_SMALL_15 = 19
    CATEGORY_TRAILER_LARGE_15 = 20
    CATEGORY_REPAIRMAN = 21
    CATEGORY_TRICIMOTO = 22
    CATEGORY_SELLER_AUTO = 23

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150))
    brand_id = db.Column(db.Integer, db.ForeignKey('car_brand.id'))
    category = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger, default=1)
    car_type = db.Column(db.Unicode(50))
    
    brand = db.relationship('CarBrand')


    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'CarModel({})'.format(self.id)
