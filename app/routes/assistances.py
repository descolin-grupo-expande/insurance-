from flask import Blueprint, request, jsonify
from app.extensions import db
from app import models as m

from app.svc import assistance as assistance_svc
from app.svc import assistance_api_svc as api_svc
from app.svc import assistance_app_c_svc as assistance_client_svc
from app.svc import assistanceticket as assistance_ticket_svc
from app.svc import assistancecase as assistance_case_svc
from app.errors import errors
from datetime import datetime

assistances_bp = Blueprint('assistances_bp', __name__)

@assistances_bp.route('/client/svc/available', methods=['POST'])
def listAvailableServices():
    """
    lists all available services to a client under the campaign_id 
    """
    sentInfo = request.get_json()
    
    client = assistance_client_svc.client_nation_campaign(sentInfo)

    if client.status != m.User.STATUS_ACTIVE:
        return api_svc.errors(16)
    if client:
        vial, medical, home, legal, special, funeral, laboral, dental, exam, veterinarian, travel = [], [], [], [], [], [], [], [], [], [], []
        other = []
        total_assistances = []
        
        member_ids = assistance_client_svc.get_user_member_relation(client.id)
    
        for i in range(len(member_ids)):
            print(member_ids[i].member_id)
            assistances = assistance_svc.get_assistance_plan_service_types(member_ids[i].member_id, sentInfo["campaign_id"])
            for j in range(len(assistances)):
                total_assistances.append(assistances[j])
        print(member_ids)
        
        for assistance in total_assistances:
            print('categoyr: ', assistance["assistance_service_category"])
            if assistance["assistance_service_category"] == "Vial":
                vial.append(assistance)
            elif assistance["assistance_service_category"] == "Hogar":
                home.append(assistance)
            elif assistance["assistance_service_category"] == "Especiales":
                special.append(assistance)
            elif assistance["assistance_service_category"] == "Funeraria":
                funeral.append(assistance)
            elif assistance["assistance_service_category"] == "Médica":
                medical.append(assistance)
            elif assistance["assistance_service_category"] == "Veterinaria":
                veterinarian.append(assistance)
            elif assistance["assistance_service_category"] == "Legal":
                legal.append(assistance)
            elif assistance["assistance_service_category"] == "Asistencia en Viajes":
                travel.append(assistance)
            else:
                other.append(assistance)
        
        all_assistances = {
            "Vial":vial,
            "Hogar":home,
            "Médica":medical,
            "Legal": legal,
            "Funeraria":funeral,
            "Veterinaria": veterinarian,
            "Especiales":special,
            "Asistencia en Viajes":travel
        }
        if len(other) > 0:
            all_assistances["Otros"] = other

        categories_info = assistance_svc.get_assistances_categories_info()

        if len(total_assistances) == 0:
            return api_svc.success("No Services available", {"assistances":all_assistances}, status=919)    
        else:
            return api_svc.success("services retrieved",{"assistances":all_assistances, "categories_info" : categories_info})
    else:
        return api_svc.errors(3)
    

@assistances_bp.route('/client/svc/start', methods=['POST'])
def startService():
    """
    starts an assistance case
    """
    sentInfo = request.get_json()
    rsp = assistance_client_svc.start_case(sentInfo)
    
    if rsp == 3:
        return api_svc.errors(3)
    elif rsp == 7:
        return api_svc.errors(7)
    elif rsp == 17:
        return api_svc.errors(17)
    elif isinstance(rsp,int) and (rsp>= 24 and rsp <=28):
        print("->IS ERROR")
        return api_svc.errors(rsp)
    elif rsp == 24:
        return api_svc.errors(rsp)
    else:
        return api_svc.success("service started", rsp)
    
@assistances_bp.route('/client/cancel', methods=['POST'])
def cancelAssistanceApp():
    """
    {
        "case_id":0,
        "user_id":0,
        "service_id":0,
        "ticket_type":0

    }
    """
    case_info = request.get_json()
    can_cancel_assistance = False
    print("case_info",case_info)
    tickets = db.session.execute(db.select(m.AssistanceTicket).where(m.AssistanceTicket.case_id == case_info["case_id"])).scalars().all()
    for ticket in tickets:
        if ticket.ticket_type == m.AssistanceTicket.ASSIGN_PROVIDER:
            #If has provider return response that is we cannot cancel assisance
            print("Has Provider",ticket.ticket_type)
            can_cancel_assistance = False
            return api_svc.errors(18)
        else:
            can_cancel_assistance = True

    if can_cancel_assistance == True:
        cancel_by_user_ticket = assistance_ticket_svc.create_new_assistance_ticket(case_info)
        print("Is not Provider",ticket.ticket_type)
        assistance_case = db.session.query(m.AssistanceCase).get(case_info["case_id"])
        assistance_case = db.session.get(m.AssistanceCase,case_info["case_id"])
        if not assistance_case:
            raise errors.not_found_error
    
        # If case is already close just return it
        if assistance_case.status == m.AssistanceCase.STATUS_CLOSE:
            return assistance_case

        # Close case
        assistance_case.status = m.AssistanceCase.STATUS_CLOSE
        assistance_case.date_end = datetime.utcnow()

        assistance_case_svc.close_tickets(assistance_case.id)
        return api_svc.success("Assistance canceled successfully")
    else:
        return api_svc.errors(18)