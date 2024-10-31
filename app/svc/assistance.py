from app.extensions import db
from app import models as m
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from app.svc import assistancecase as assistance_case_svc

def nonNegativeInt(number):
    try:
        number = int(number)

        if number >= 0:
            return number
    except Exception as e:
        pass

    return 0

def get_assistance_plan_service_types(member_id, campaign_id):
    """
    returns 
    service id service name, service category name
    planservice max assistance
    assistance plan waiting period
    """

    response, data = [], []
    member_assistances = db.session.execute(db.select(
        m.AssistanceService.id, #0
        m.AssistanceService.name, #1
        m.AssistanceCategory.name, #2
        m.AssistancePlanService.max_assistance, #3
        m.AssistancePlanService.waiting_period, #4
        m.AssistancePlan.id, #5
        m.AssistanceSale.id, #6
        m.AssistancePlan.coverage_name, #7
        m.AssistanceSale.date_effective, #8
        m.AssistanceCategory.id, #9
        m.Assistance.id, #10
        m.AssistanceService.description, #11
        m.AssistancePlanService.max_assistance_period, #12
        m.AssistanceService.app_required_delivery, #13
        m.AssistanceCategory.image_url, #14
        m.AssistanceService.image_url #15
    ).join(
        m.AssistanceCategory
    ).join(
        m.AssistancePlanService
    ).join(
        m.AssistancePlan
    ).join(
        m.AssistanceSale
    ).join(
        m.Assistance
    )
    .where(
        m.AssistanceSale.member_id == member_id,
        m.AssistanceService.status_app == m.AssistanceService.STATUS_APP_ACTIVE,
        m.AssistanceSale.status == 1,
        m.Assistance.sponsor_id == campaign_id
    )).all()

    print(member_assistances)
    current_time = datetime.now() 
    for i in member_assistances:
        obj = {}
        sale = db.session.get(m.AssistanceSale, i[6])
        from_date = None
        if i[12] == m.AssistancePlanService.ANNUAL_PERIOD:
            # Use the current year as period
            compare_date = date(date.today().year, sale.date_effective.month, sale.date_effective.day)
            if compare_date <= current_time.date():
                from_date = compare_date
            else:
                from_date = date(date.today().year - 1, sale.date_effective.month, sale.date_effective.day)
        elif i[12] == m.AssistancePlanService.MONTHLY_PERIOD:
            # Use current month as period
            compare_date = date(date.today().year, date.today().month, sale.date_effective.day)
            if compare_date <= current_time.date():
                from_date = compare_date
            else:
                from_date = date(date.today().year, date.today().month - 1, sale.date_effective.day)
        if from_date:
            print('From_date: ' + from_date.strftime("%d/%m/%Y, %H:%M:%S")) 
            # used_services = assistance_ticket_svc\
            #     .count_valid_services_by_member_service_sale(
            #         [member_id], i[0], i[6], date_from=from_date
            #     )
            used_services = assistance_case_svc \
                .count_valid_services_by_member_service_sale(
                    [member_id], i[0], i[6], date_from=from_date
                )
            print('used_services: ' + str(used_services))
            if i[3] == None:
                remaining_assistances = 100
            else:
                remaining_assistances = i[3] - used_services
                remaining_assistances = nonNegativeInt(remaining_assistances)

            # waiting period == null
            if i[4] == None:
                wp = 0
            else:
                wp = i[4]

            assistance_activation = i[8] + relativedelta(months=+wp)
            #obj build 
            obj["assistance_service_id"] = i[0]
            obj["assistance_service_name"] = i[1]
            obj["assistance_service_category"] = i[2]
            #obj["assistance_service_max_services"] = i[3]
            #obj["assistance_service_category_id"] = i[9]
            obj["assistance_activation_date"] = assistance_activation
            obj["remaining_service_assistances"] = remaining_assistances
            obj["sale_id"] = i[6]
            obj["plan_id"] = i[5]
            obj["assistance_id"] = i[10]
            obj["description"] = i[11]
            obj["requires_delivery"] = i[13]
            obj["category_image_url"] = i[14]
            obj["assistance_image_url"] = i[15]
            #obj["date effective"]= i[8]
            #obj["waiting time"]= i[4]
            data.append(obj)
    for i in data:
        assistance = i
        if len(response) == 0:
            response.append(assistance)
        else:
            for j in range(len(response)):
                approved = False
                comp = response[j]
                if comp["assistance_service_name"] == assistance["assistance_service_name"]:
                    newVal = comp["remaining_service_assistances"] + assistance["remaining_service_assistances"]
                    comp["remaining_service_assistances"] = newVal
                    if comp["assistance_activation_date"]>assistance["assistance_activation_date"]:
                        comp["assistance_activation_date"] = assistance["assistance_activation_date"]
                        comp["sale_id"] = assistance["sale_id"]
                        comp["plan_id"] = assistance["plan_id"] 
                    data.pop(data.index(i))
                    break
                else:
                    approved = True
            if approved == True:
                response.append(assistance)   
    return response

def get_assistances_categories_info():

    categories = db.session.execute(db.select(m.AssistanceCategory)).scalars().all()
    categories_dic = {}

    for i in categories:
        categories_dic[i.name] = {}
        categories_dic[i.name]['priority'] = i.priority
        categories_dic[i.name]['image_url'] = i.image_url

    return categories_dic