from app.extensions import db

class AssistanceSaleCar(db.Model):
    """Docstring for AssistanceSaleCar.
        car_color
            1=White
            2=Silver
            3=Black
            4=Gray
            5=Blue
            6=Red
            7=Brown
            8=Green
            9=Orange
            10=Pink
    """

    COLOR_WHITE = 1
    COLOR_SILVER = 2
    COLOR_BLACK = 3
    COLOR_GRAY = 4
    COLOR_BLUE = 5
    COLOR_RED = 6
    COLOR_BROWN = 7
    COLOR_GREEN = 8
    COLOR_ORANGE = 9
    COLOR_PINK = 10

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assistance_sale_id = db.Column(db.Integer, db.ForeignKey('assistance_sale.id'))
    car_model_id = db.Column(db.Integer, db.ForeignKey('car_model.id'))
    car_color = db.Column(db.SmallInteger)
    car_plate = db.Column(db.Unicode(20))
    car_year = db.Column(db.Integer)
    brand_description = db.Column(db.Unicode(100))
    type_description = db.Column(db.Unicode(100))
    model_description = db.Column(db.Unicode(100))
    color_description = db.Column(db.Unicode(100))
    serial_number = db.Column(db.Unicode(100))
    engine_number = db.Column(db.Unicode(100))
    status = db.Column(db.SmallInteger)

    car_model = db.relationship('CarModel')

    def __str__(self):
        return f'AssistanceSaleCar: {self.car_model_id}, {self.car_color}, {self.model_description}, {self.car_plate}, {self.serial_number}, {self.car_year}'

