from app.extensions import db
from app import models as m
from app.config import config

from app.svc import assistance_api_svc as api_svc
from app.svc import assistancecase as assistance_case_svc

def client_nation_campaign(sentInfo):
    """
    query user by national_id and campaign_id
    """
    # check if request comes from teledoctor to search
    # a teledoctor user type or a common user 
    if "teledoctor_user_id" in sentInfo:
        client = db.session.execute(db.select(m.User).where(m.User.id == sentInfo["teledoctor_user_id"])).scalar()
    else:
        client = db.session.execute(db.select(m.User).where(
            m.User.national_id == sentInfo["national_id"],
            m.User.campaign_id == sentInfo["campaign_id"],
            m.User.user_type == m.User.USER_TYPE_CLIENT
        )).scalar()
    return client

def get_umr_member_id(user_id):
    """
    query all members id by user id
    """
    members = db.session.execute(db.select(m.MemberUserRelation.member_id).where(m.MemberUserRelation.user_id == user_id)).scalars().all()
    return members

def search_in_members_and_match_with_sale(member_ids, sale_id):

    """
    Sometimes a user has many members (it should only have one) so we have to search for the correct member that is assigned 
    to the assistance_sale, otherwise it will throw an error saying : {"status": "907", "message": "Error: wrong case data sent"}
    """

    sale = db.session.execute(db.select(m.AssistanceSale).where(m.AssistanceSale.id == sale_id)).scalar()
    for id in member_ids:
        if id == sale.member_id: #id its a tuple from sql-alchemy
            return id
    return -1 

def addCar(sentInfo):
    """
    register car to member

    @input_params(JSON):
    national_id, car_model_id, car_color, car_plate, car_year,

    @returns:
    0

    @errors:
    -1, 19
    """
    try:
        member = db.session.execute(db.select(m.Member).where(m.Member.national_id == sentInfo['national_id'])).scalar()
        print('member: ', member)

        # Aliases para subconsultas
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

        for spo in assistance_sale:
            sale_id = spo.id
         
        if assistance_sale != None:
            assistance_sale_car = m.AssistanceSaleCar(
                assistance_sale_id = sale_id,
                car_model_id = sentInfo["car_model_id"],
                car_color = sentInfo["car_color"],
                car_plate = sentInfo["car_plate"],
                car_year = sentInfo["car_year"],
                status = 1
            )
            db.session.add(assistance_sale_car)
            db.session.flush()
            db.session.commit()
            return 0
        else:
            print('dont have assistance sale')
            return 19
    except Exception as e:
        print("Exception occurred:", e)
        return -1
    
def get_user_member_relation(user_id):
    """
    query all user x members  relationship by user id
    """
    members = db.session.execute(db.select(m.MemberUserRelation).where(m.MemberUserRelation.user_id == user_id)).scalars().all()

    return members

def start_case(sentInfo):
    """
    creates case and first ticket

    @input_params(JSON):
    campaign_id, latitude, longitude, assistance_id, assistance_service_id, location, national_id, plan_id, sale_id, car_data

    @returns:
    case_id, provider arrival code

    @errors:
    17, 7, 3
    """
    client = client_nation_campaign(sentInfo)    
    if client:
        member_ids = get_umr_member_id(client.id)
            
        if len(member_ids) == 0:
            return 17

        if len(member_ids) > 0:

            member_id_of_sale = search_in_members_and_match_with_sale(member_ids, sentInfo["sale_id"])
            
            if member_id_of_sale == -1:
                return 17 ##Error: User does not match any members

            member = db.session.execute(db.select(m.Member).where(m.Member.id == member_id_of_sale)).scalar()

            case_data = {}
            
            if "teledoctor_sale_id" in sentInfo:
                sale_id = sentInfo["teledoctor_sale_id"]
                sale = db.session.execute(db.select(m.AssistanceSale).where(m.AssistanceSale.id == sale_id)).scalar()
                plan = db.session.execute(db.select(m.AssistancePlan).where(m.AssistancePlan.id == sale.assistance_plan_id)).scalar()
                
                assistance_id = plan.assistance_id
                plan_id = sale.assistance_plan_id
                case_data["is_teledoctor"] = True

            else:
                sale_id = sentInfo["sale_id"]
                assistance_id = sentInfo["assistance_id"]
                plan_id = sentInfo["plan_id"]
                case_data["is_teledoctor"] = False

            case_data["phone"] = client.phone_number
            case_data["member_id"] = member.id
            case_data["address"] = sentInfo["location"] + " Coordenadas: lat: " +str(sentInfo["latitude"]) + " lon: " +str(sentInfo["longitude"])
            case_data["latitude"] = sentInfo["latitude"]
            case_data["longitude"] = sentInfo["longitude"]
            case_data["contact_name"] = member.name
            case_data["applicant_name"] = sentInfo.get("applicant_name", member.name)
            case_data["member_status"] = member.status
            case_data["assistance_id"] = assistance_id
            case_data["member"] = None
            case_data["assistance_sale_id"] = sale_id
            case_data["assistance_plan_id"] = plan_id
            case_data["is_app"] = True
            case_data["client_id"] = client.id
            case_data["country_id"] = member.country

            
            if "address_destination" in sentInfo:
                case_data["destination_latitude"] = sentInfo["destination_latitude"]
                case_data["destination_longitude"] = sentInfo["destination_longitude"]
            else:
                sentInfo["address_destination"] = None

            # Created by user id client
            case_data["created_by_user_id"] = client.id 

            code = api_svc.create_pin()
            ticket_data = {}
            if "teledoctor_sale_id" in sentInfo:
                origin = " Consulta Medica: " + str(sentInfo["teledoctor_consultation_id"])
                ticket_data["comment"] = config.IN_APP_TD_TICKET_TYPE_1_COMMENT + origin

            else:
                txt = config.IN_APP_TICKET_TYPE_1_COMMENT
                if sentInfo["comment"] != "":
                    txt = txt + " El cliente dijo: '"+sentInfo["comment"]+"'"
                ticket_data["comment"] = txt

            ticket_data["datetime"] = None
            ticket_data["service_id"] = sentInfo["assistance_service_id"]
            ticket_data["ticket_type"] = 1
            ticket_data["user_id"] = client.id
            ticket_data["address_destination"] = sentInfo["address_destination"]
            ticket_data["provider_arrival_code"] = code
            ticket_data["latitude"] = sentInfo["latitude"]
            ticket_data["longitude"] = sentInfo["longitude"]
            ticket_data["fromApp"] = True
            a = {}
            if sentInfo["car_data"] != a:
                ticket_data["car_model_id"] = sentInfo["car_data"]["car_model_id"]
                ticket_data["car_year"] =  sentInfo["car_data"]["car_year"]
                ticket_data["car_plate"] = sentInfo["car_data"]["car_plate"]
                ticket_data["car_color"] = sentInfo["car_data"]["car_color"]
            else:
                ticket_data["car_model_id"] = None
                ticket_data["car_year"] =  None
                ticket_data["car_plate"] = None
                ticket_data["car_color"] = None

            print("case_data_app", case_data)
            print("ticket_data_app", ticket_data)    
            case,new_ticket = assistance_case_svc.create_initial_case_ticket(case_data,ticket_data)
                
            if case == False:
                return 7
            else:
                print('else')
                
                code = api_svc.create_pin()
                if "teledoctor_sale_id" not in sentInfo:
                    app_case = m.AssistanceAppCase(
                        assistance_case_id =case.id,
                        assistance_service_id =sentInfo["assistance_service_id"],
                        latitude = sentInfo["latitude"],
                        longitude = sentInfo["longitude"])
                    db.session.add(app_case)
                db.session.flush()
                db.session.commit()

                return {"case_id":case.id, "provider_code":ticket_data["provider_arrival_code"]}

        else:
            return 3
    
    else:
        return 3


def unassignCar(sentInfo):
    """
    unassign a car to member

    @input_params(JSON):
    assistance_sale_id,

    @returns:
    0

    @errors:
    -1, 19
    """
    try:
        print('assistance_sale: ', sentInfo['assistance_sale_car_id'])
        assistance_sale_car = db.session.execute(db.select(m.AssistanceSaleCar).where(
            m.AssistanceSaleCar.id == sentInfo['assistance_sale_car_id']
        )).scalar()

        setattr(assistance_sale_car, 'status', 0)
        db.session.flush()
        db.session.commit()
        return 0
    except Exception as e:
        print("Error ",e)
        return -1