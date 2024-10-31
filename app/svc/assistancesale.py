from app.extensions import db
from app import models as m

def create_car(sale_car_dict, extra_dataCar):
    if extra_dataCar.get('model'):
        model = str(extra_dataCar.get('model')).strip().upper()
        car_model = db.session.execute(
            db.select(m.CarModel)
            .where(db.func.upper(m.CarModel.name) == model)
            .order_by(m.CarModel.id.desc())
        ).scalar()

        if not car_model:
            car_brand = None

            if extra_dataCar.get('brand'):
                brand = str(extra_dataCar.get('brand')).strip().upper()
                car_brand = db.session.execute(
                    db.select(m.CarBrand)
                    .where(db.func.upper(m.CarBrand.name) == brand)
                    .order_by(m.CarBrand.id.desc())
                ).scalar()

            if not car_brand:
                car_brand = m.CarBrand(
                    name = brand,
                    priority = 1
                )
                db.session.add(car_brand)
                db.session.flush()

            car_model = m.CarModel(
                name = model,
                brand_id = car_brand.id,
                category = m.CarModel.CATEGORY_AUTO
            )
            db.session.add(car_model)
            db.session.flush()

        sale_car_dict['car_model_id'] = car_model.id


def create_car_color(sale_car_dict, extra_dataCar):
    if extra_dataCar.get('color'):
        color =  str(extra_dataCar.get('color')).strip().upper()

        car_color = db.session.execute(
            db.select(m.Catalog)
            .where(
                m.Catalog.grouper == "CAR_COLOR",
                db.or_(db.func.upper(m.Catalog.description_es) == color,db.func.upper(m.Catalog.description_en) == color)
            )
            .order_by(m.Catalog.id.desc())
        ).scalar()

        if not car_color:
            car_color_code = db.session.execute(
                db.select(m.Catalog)
                .where(m.Catalog.grouper == "CAR_COLOR")
                .order_by(m.Catalog.code.desc())
            ).scalar()

            car_color = m.Catalog(
                grouper="CAR_COLOR",
                code=int(car_color_code.code) + 1,
                description_es=color,
                description_en=color
            )
            db.session.add(car_color)
            db.session.flush()

        sale_car_dict['car_color'] = car_color.code