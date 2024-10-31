from flask import Blueprint, request, jsonify
from app.extensions import db
from app.decorator.decorators import iterable
from app import models as m
from app.requestfilter.iterator import get_default_iterator
from app.svc import assistance_api_svc as api_svc
from app.svc import assistance_app_c_svc as assistance_client_svc

from datetime import datetime

cars_bp = Blueprint('cars_bp', __name__)

@cars_bp.route('/color', methods=['GET'])
def getColors():
    client_language = db.session.execute(db.select(m.User.ui_language).where(m.User.id == 26)).scalar() # QUEMADO
    
    car_colors = db.session.execute(db.select(m.CarColor).where(
        m.CarColor.language == client_language
    )).scalars().all()

    car_colors_list = [color.to_dict() for color in car_colors]

    return jsonify(car_colors_list)
    
@cars_bp.route('/brands', methods=['GET'])
@iterable(sort_fields=['priority'])
def get_cars_brands():
    """TODO: Docstring for get_cars_brands.
    :returns: TODO

    """
    print('all brands')
    return get_default_iterator(m.CarBrand)

@cars_bp.route('/brands/<int:car_brand_id>/models', methods=['GET'])
def get_car_brand_models(car_brand_id):
    """Obtiene los modelos de autos para una marca específica.

    :car_brand_id: ID de la marca de auto
    :returns: Lista de modelos de autos activos
    """
    vehicle_type = request.args.get("category")
    name_model = request.args.get("nameModel")

    print('vehicle_type', vehicle_type)
    print('nameModel', name_model)

    # Obtener la marca del auto
    car_brand = db.session.get(m.CarBrand, car_brand_id)

    if not car_brand:
        return {"error": "Car brand not found"}, 404

    # Verificar y agregar un nuevo modelo si se proporciona un nombre
    if name_model:
        name_model = name_model.strip()

        exist_car_models = db.session.execute(
            db.select(m.CarModel).where(
                m.CarModel.brand_id == car_brand.id,
                m.CarModel.status == m.CarModel.STATUS_ACTIVE,
                m.CarModel.name == name_model
            )
        ).scalars().all()

        if not exist_car_models:
            car_model = m.CarModel(
                name=name_model,
                brand_id=car_brand_id,
                category=1,
            )
            db.session.add(car_model)
            db.session.flush()  # Flushea para asegurar que se guarde en la base de datos

    # Consulta de los modelos activos de la marca
    car_models_query = (
        db.session.query(m.CarModel).where(
            m.CarModel.brand_id == car_brand.id,
            m.CarModel.status == m.CarModel.STATUS_ACTIVE
        )
    )

    # Filtrar por tipo de vehículo si se proporciona
    if vehicle_type is not None:
        car_models_query = car_models_query.where(m.CarModel.category == vehicle_type)

    # Ordenar y obtener todos los modelos
    car_models = car_models_query.order_by(m.CarModel.name.asc()).all()
    
    # Convertir a una lista de diccionarios
    car_models_list = [model.__dict__ for model in car_models]
    
    # Eliminar la clave _sa_instance_state que es innecesaria en la respuesta
    for model in car_models_list:
        model.pop('_sa_instance_state', None)

    return car_models_list

@cars_bp.route('/years', methods=['GET'])
def sendYears():
    now = datetime.now()
    year = int(now.year) + 2
    years = []
    for i in range(1950, year):
        years.append(i)
    years.sort(reverse = True)
    return api_svc.success("years generated", {"years":years})

@cars_bp.route('/client/addcar', methods=['POST'])
def addCar():
    """
    REGISTER CAR FOR ASSISTANCE
    """
    sentInfo = request.get_json()
    print('sentInfo: ', sentInfo)
    rsp = assistance_client_svc.addCar(sentInfo)
    print('rsp: ', rsp)
    if rsp == 0:
        return api_svc.success("vehicle added", rsp)
    else:
        return api_svc.errors(rsp)
    

@cars_bp.route('/client/car', methods=['GET'])
def getCars():  
    
    client = db.session.execute(db.select(m.User).where(m.User.id == 1802866)).scalar()

    if client:
        member = db.session.execute(db.select(m.Member).where(
            m.Member.national_id == client.national_id,
        )).scalar()

        assistance_sale = None
        car_status = 1
        
        client_language = db.session.execute(db.select(m.User.ui_language).where(
            m.User.id == client.id
        )).scalar()

        car_colors = db.session.execute(db.select(m.CarColor).where(
            m.CarColor.language == client_language
        )).scalars().all()
            
        print("car_colors",car_colors)
        result = []

        AssistanceSaleAlias = db.aliased(m.AssistanceSale)
        AssistancePlanAlias = db.aliased(m.AssistancePlan)
        AssistancePlanServiceAlias = db.aliased(m.AssistancePlanService)
        AssistanceServiceAlias = db.aliased(m.AssistanceService)

        # Subconsulta para obtener IDs de `AssistanceService` con `category_id IN (2, 21)`
        assistance_service_subquery = (
            db.select(AssistanceServiceAlias.id)
            .where(AssistanceServiceAlias.category_id.in_([2, 21]))
        ).subquery()

        # Subconsulta para obtener IDs de `AssistancePlanService` que coincidan con los servicios en la subconsulta anterior
        assistance_plan_service_subquery = (
            db.select(AssistancePlanServiceAlias.plan_id)
            .where(AssistancePlanServiceAlias.service_id.in_(assistance_service_subquery))
            .distinct()
        ).subquery()

        # Subconsulta para obtener `AssistancePlan` IDs que coincidan con `AssistancePlanService`
        assistance_plan_subquery = (
            db.select(AssistancePlanAlias.id)
            .where(AssistancePlanAlias.id.in_(assistance_plan_service_subquery))
        ).subquery()

        # Consulta principal para obtener `AssistanceSale`
        assistance_sale = db.session.execute(
            db.select(AssistanceSaleAlias)
            .where(
                AssistanceSaleAlias.member_id == member.id,
                AssistanceSaleAlias.assistance_plan_id.in_(assistance_plan_subquery)
            )
        ).scalars().all()

        cars = []
        for spo in assistance_sale:
            if assistance_sale != None:
                assistance_sale_car_full = db.session.execute(
                    db.select(
                        m.AssistanceSaleCar.id.label('assistance_sale_id'),
                        m.AssistanceSaleCar.car_color.label('car_color'),
                        m.AssistanceSaleCar.car_model_id.label('car_model_id'),
                        m.AssistanceSaleCar.car_plate.label('car_plate'),
                        m.AssistanceSaleCar.car_year.label('car_year'),
                        m.CarModel.name.label('car_model_name'),
                        m.CarBrand.id.label('car_brand_id'),
                        m.CarBrand.name.label('car_brand_name'),
                        m.AssistanceSaleCar.car_plate.label('car_plate'),
                        m.AssistanceSaleCar.car_year.label('car_year')
                    )
                    .join(m.CarModel, m.AssistanceSaleCar.car_model_id == m.CarModel.id) \
                    .join(m.CarBrand, m.CarModel.brand_id == m.CarBrand.id) \
                    .where(
                        m.AssistanceSaleCar.assistance_sale_id == spo.id,
                        m.AssistanceSaleCar.status == car_status,
                    )
                ).all()

                if len(assistance_sale_car_full) is not 0: 
                    for c in assistance_sale_car_full:
                        cars.append(c)

        for d in cars:
            color_name = car_colors[d.car_color -1 ].name
                
            tempdata = {
                'assistance_sale_id': d.assistance_sale_id,
                'itemColor': {
                    'id': d.car_color,
                    'name': color_name,
                },
                'itemBrand': {
                    'id': d.car_brand_id,
                    'name': d.car_brand_name,
                },
                'itemModel': {
                    'id': d.car_model_id,
                    'name': d.car_model_name,
                },
                'registration': d.car_plate,
                'year': d.car_year
            }
            result.append(tempdata)
        return result
    else:
        return api_svc.errors(3)
    
@cars_bp.route('/client/car/unassign', methods=['POST'])
def unassignCar():
    """
    UNASSIGN CAR FOR ASSISTANCE
    """
    sentInfo = request.get_json()
    print('sentInfo: ', sentInfo)
    rsp = assistance_client_svc.unassignCar(sentInfo)
    print('rsp: ', rsp)
    if rsp == 0:
        return api_svc.success("vehicle unassigned", rsp)
    else:
        return api_svc.errors(rsp)