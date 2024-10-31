from app.extensions import db
from app.config import config
from app import models as m
import traceback
import calendar
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from app.errors import errors
from app.svc import assistanceticket as assistance_ticket_svc
from app.svc import member as member_svc
from app.svc import country as country_svc

def count_valid_services_by_member_service_sale(
    member_ids, service_id, sale_id, date_from=None, date_to=None):
    """"
        Get how many valid services has the member had by service and member id

        @param member_ids int[] array of ids of member to look cases from
        @param service_id int service to look tickets of
        @param sale_id int id of sale to count services of
        @param date_from datetime minimum date of date_start of cases
        @param date_to datetime maximum date of date_start of cases
        @return int amount of services for that members, service, sale within
        the date ranges
    """
    # First get the id of the cases of the services that have the service
    service_case_ids = get_closed_case_ids_by_member_sale_service_types(
        member_ids, service_id, sale_id, [m.AssistanceTicket.ASSIGN_SERVICE],
        date_from, date_to
    )

    # Get the id of the cases that have been canceled
    canceled_ids = get_closed_case_ids_by_member_sale_service_types(
        member_ids, service_id, sale_id, [
            m.AssistanceTicket.CANCELED_BY_CLIENT_WITHOUT_COST,
            m.AssistanceTicket.REIMBURSE
        ], date_from, date_to
    )

    # Get the id of the cases that are by connection
    connection_ids = get_closed_case_ids_by_member_sale_service_types(
        member_ids, service_id, sale_id, [m.AssistanceTicket.CONNECTION],
        date_from, date_to
    )

    courtesy_ids = get_courtesy_case_ids_by_member_sale_service_types(
        member_ids, service_id, sale_id, [m.AssistanceTicket.COURTESY_ASSISTANCE],
        date_from, date_to
    )

    # The amount of services is the service case id - canceled ids - connection id 
    valid_case_ids = list(
        set(service_case_ids)  - set(canceled_ids) - set(connection_ids)  - set(courtesy_ids)
    )
    courtesy_case_ids = list(
       set(courtesy_ids)
    )



    if valid_case_ids:
        return len(valid_case_ids)

    return 0

def get_closed_case_ids_by_member_sale_service_types(
    member_ids, service_id, sale_id, types, date_from, date_to):
    query = db.session.query(
            m.AssistanceCase.id, m.AssistanceTicket.service_id
        ) \
        .filter(
            m.AssistanceCase.member_id.in_(member_ids),
            m.AssistanceTicket.service_id == service_id,
            m.AssistanceCase.assistance_sale_id == sale_id,
            m.AssistanceCase.status == m.AssistanceCase.STATUS_CLOSE,
            m.AssistanceTicket.ticket_type.in_(types),
            m.AssistanceCase.id == m.AssistanceTicket.case_id
        )

    # Get info for reimbursement cases with amount registered
    query2 = None
    if m.AssistanceTicket.REIMBURSE in types:
        query2 = db.session.query(
                m.AssistanceCase.id, m.AssistanceTicket.service_id
            ) \
            .filter(
                m.AssistanceCase.member_id.in_(member_ids),
                m.AssistanceTicket.service_id == service_id,
                m.AssistanceCase.assistance_sale_id == sale_id,
                m.AssistanceCase.status == m.AssistanceCase.STATUS_CLOSE,
                m.AssistanceCase.id == m.AssistanceTicket.case_id,
                m.AssistanceCase.reimbursement_amount != None
            )

    # Add possible fields
    if date_from:
        query = query.filter(
            m.AssistanceTicket.datetime >= date_from
        )
        if query2:
            query2 = query2.filter(
                m.AssistanceTicket.datetime >= date_from
            )

    if date_to:
        query = query.filter(
            m.AssistanceTicket.datetime < date_to
        )

        if query2:
            query2 = query2.filter(
                m.AssistanceTicket.datetime < date_to
            )

    if query2:
        # Finish query and get results reimburse
        query2 = query2.group_by(
            m.AssistanceCase.id,
            m.AssistanceTicket.service_id
        )
        data2 = query2.all()

        # Prepare array of case ids reimburse
        case_ids_reimburse = []
        for info in data2:
            case_ids_reimburse.append(info[0])

        # Exclude reimbursement cases
        query = query.filter(
            ~m.AssistanceCase.id.in_(case_ids_reimburse)
        )

    # Finish query and get results
    query = query.group_by(
        m.AssistanceCase.id,
        m.AssistanceTicket.service_id
    )

    data = query.all()

    # Prepare array of case ids
    case_ids = []
    for info in data:
        case_ids.append(info[0])

    return case_ids
    
def get_courtesy_case_ids_by_member_sale_service_types(
    member_ids, service_id, sale_id, types, date_from, date_to):
    query = db.session.query(
            m.AssistanceCase.id, m.AssistanceTicket.service_id
        ) \
        .filter(
            m.AssistanceCase.member_id.in_(member_ids),
            m.AssistanceTicket.service_id == service_id,
            m.AssistanceCase.assistance_sale_id == sale_id,
            m.AssistanceCase.status == m.AssistanceCase.STATUS_CLOSE,
            m.AssistanceTicket.ticket_type.in_(types),
            m.AssistanceCase.id == m.AssistanceTicket.case_id
        )

    # Add possible fields
    if date_from:
        query = query.filter(
            m.AssistanceTicket.datetime >= date_from
        )

    if date_to:
        query = query.filter(
            m.AssistanceTicket.datetime < date_to
        )

    # Finish query and get results
    query = query.group_by(
        m.AssistanceCase.id,
        m.AssistanceTicket.service_id
    )

    data = query.all()

    # Prepare array of case ids
    case_ids = []
    for info in data:
        case_ids.append(info[0])

    return case_ids

def create_initial_case_ticket(data, first_ticket=None):
    """
    create initial case tickets, if member is new it creates one.
    """
    print("\n\n\ncase data", data)
    print("\n\n\ncase ticket", first_ticket)


    if data['member'] is not None:
        member = member_svc.create_edit(data['member'])
        
        if member.id is None:
            # New member, add to DB
            db.session.add(member)
            db.session.flush()
            member_id = member.id
        else:
            member_id = member.id

    elif data['member_id'] is not None:
        member_id = data['member_id']

    sale_id = data.get('assistance_sale_id')
    plan_id = data.get('assistance_plan_id')

    # Validate the sale
    error = validate_sale(
        sale_id, member_id, plan_id
    )

    if error:
        return False, False


    if 'destination_latitude' in data:
        temp_lat = data["destination_latitude"]
    else:
        temp_lat = None
    
    if 'destination_longitude' in data:
        temp_long = data["destination_longitude"]
    else:
        temp_long = None

    # Validate if first_ticket data in payload
    # If this assistance case can will created by bellow methods
    if first_ticket:
        connection = first_ticket.get('connection')
        create_connection_ticket = (connection == 1)

        if first_ticket.get("latitude") and first_ticket.get("longitude"):
            temp_lat = first_ticket.get("latitude")
            temp_long = first_ticket.get("longitude")

        can_create_assistance_case, error = validate_creation_assistance_case(
            create_connection_ticket, sale_id, first_ticket["service_id"], plan_id, member_id
        )

        if not can_create_assistance_case:
            print(str(traceback.format_exc()))
            exception_return = {
                'error': error,
                'status': 0,
            }
            return exception_return, 0

    assistance_case = m.AssistanceCase(
        member_id=member_id,
        country_id=data.get('country_id'),
        state_id=data.get('state_id'),
        assistance_id=data.get('assistance_id'),
        assistance_plan_id=plan_id,
        assistance_sale_id=sale_id,
        address=data.get('address'),
        phone=data.get('phone'),
        phone2=data.get('phone2'),
        email = data.get('email'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        member_comment=data.get('member_comment'),
        case_ticket_info=data.get('case_ticket_info'),
        status=data.get('status'),
        contact_channel=data.get('contact_channel'),
        date_start=data.get('date_start'),
        contact_name=data.get('contact_name'),
        applicant_name=data.get('applicant_name'),
        member_status=data.get('member_status'),
        zone=data.get('zone'),
        area=data.get('area'),
        state_district_id=data.get('state_district_id'),
        destination_latitude = temp_lat,
        destination_longitude = temp_long,
        created_by_user_id = data.get("created_by_user_id"),
        street = data.get('street'),
        suburb = data.get('suburb'),
        postal_code = data.get('postal_code'),
        reference = data.get('reference'),
        country_phone_code = data.get('country_phone_code'),
        customer_first_name = data.get('customer_first_name'),
        customer_middle_name = data.get('customer_middle_name'),
        customer_last_name = data.get('customer_last_name'),
        customer_last_name_2 = data.get('customer_last_name_2'),
        business_name = data.get('business_name'),
        grouping_id = data.get("grouping_id"),
        grouping_chubb = data.get("grouping_chubb"),
        attendance_identifier = data.get("attendance_identifier"),
        free_text_attendance = data.get("free_text_attendance"),
        apply_survey = data.get("apply_survey"),
        apply_alerts = data.get("apply_alerts"),
        alert_mail = data.get("alert_mail"),
        item_number = data.get("item_number"),
        # sds_sinister_claim_id = sds_sinister_claim,
        origin_country_id = data.get("origin_country_id"),
        destination_country_id = data.get("destination_country_id"),
        
    )

    # Assign operator to assistance case (user logged in)
    fromApp = data.get('is_app')
    fromTeledoctorApp = data.get('is_teledoctor')
    if fromApp == True:
        assistance_case.user_id = data.get('client_id')
    else:
        assistance_case.user_id = db.session.current_user.id
        # Assign dispatcher ready to run Round Robin algorithm to assign dispatcher
        # based on last assigned job field on User model to select assistance dispatcher
        # dispatcher_id, dispatcher = get_next_dispatcher_id_online()
        # assistance_case.dispatcher_id = dispatcher_id
        # assistance_case.user_id = dispatcher_id
    
    
    db.session.add(assistance_case)
    db.session.flush()
    

    ticket_service = None

    # Create ticket service if ticket in data json
    if first_ticket:
        # Unassign user_id to assistance case
        # because this segment must assign a dispatcher
        # Unassign assistance case user_id if not new_user_id
        # This assistance case will set to not assigned to dispatcher
        assistance_case.user_id = None
        db.session.flush()

        fromApp = first_ticket.get("fromApp", False)

        # Comment showing assign user
        if assistance_case.created_by_user:
            data_ticket_assign_user = {
                "case_id": assistance_case.id,
                'ticket_type': m.AssistanceTicket.ASSIGN_UNASSIGN_USER,
                "service_id": first_ticket["service_id"],
                'comment': 'Boleta creada por {} {}'.format(
                    # g.current_user.username
                    "cliente" if fromApp else "operador",
                    assistance_case.created_by_user.username
                ),
                "fromApp": fromApp
            }
            assistance_ticket_svc.create_new_assistance_ticket(data_ticket_assign_user)

            ########################################################
            # ASSIGN OPERATOR IF FROM APP
            # If this case has created from app
            # this method will assign one operator user
            ########################################################
            if fromApp and not fromTeledoctorApp:
                operator_id, operator = assistance_ticket_svc.get_next_operator_id_online(
                    first_ticket["service_id"],
                    member_id,
                    fromApp
                )

                # If returned operator_id, else case not assigned
                if operator_id:
                    # Comment showing assign user
                    data_ticket_assign_operator = {
                        "case_id": assistance_case.id,
                        'ticket_type': m.AssistanceTicket.ASSIGN_UNASSIGN_USER,
                        "service_id": first_ticket["service_id"],
                        'comment': 'Boleta asignada a operador {}'.format(
                            operator.username
                        ),
                        "new_operator_id": operator_id,
                        "fromApp": fromApp
                    }
                    assistance_ticket_svc.create_new_assistance_ticket(data_ticket_assign_operator)


        # Assign dispatcher ready to run Round Robin algorithm to assign dispatcher
        # based on last assigned job field on User model to select assistance dispatcher
        if not fromTeledoctorApp:
            dispatcher_id, dispatcher = assistance_ticket_svc.get_next_dispatcher_id_online(
                first_ticket["service_id"],
                member_id,
                fromApp
            )

            # If returned dispatcher_id, else case not assigned
            if dispatcher_id:
                # Comment showing assign user
                data_ticket_assign_user = {
                    "case_id": assistance_case.id,
                    'ticket_type': m.AssistanceTicket.ASSIGN_UNASSIGN_USER,
                    "service_id": first_ticket["service_id"],
                    'comment': 'Boleta asignada a despachador {}'.format(
                        dispatcher.username
                    ),
                    "new_user_id": dispatcher_id,
                    "fromApp": fromApp
                }
                assistance_ticket_svc.create_new_assistance_ticket(data_ticket_assign_user)

        # Add ticket service as last step to assign
        # programmed notifications to dispatcher assigned
        first_ticket["ticket_type"] = m.AssistanceTicket.ASSIGN_SERVICE
        first_ticket["case_id"] = assistance_case.id
        new_tickets = assistance_ticket_svc.create_new_assistance_ticket(first_ticket)
        ticket_service = new_tickets[0]

        # Si no viene el caso de la app se procede a
        # desasignar al operador por orden del flujo de Promass
        # if not fromApp:
        #     setattr(assistance_case, "created_by_user_id", None)
        #     db.session.flush()

    #############################################################
    # Validate if ticket 1 is created, else raise and Exception
    #############################################################
    ticket_service_db = db.session.execute(db.select(m.AssistanceTicket.id, m.AssistanceTicket.service_id).where(
        m.AssistanceTicket.case_id == assistance_case.id,
        m.AssistanceTicket.ticket_type == m.AssistanceTicket.ASSIGN_SERVICE
    )).first()

    if not ticket_service_db:
        raise Exception("Ticket type ASSIGN_SERVICE not found")
    
    #############################################################
    # Save log on create assistance case without sale
    #############################################################
    if not assistance_case.assistance_sale_id:
        data_ticket_sale = {
            "case_id": assistance_case.id,
            'ticket_type': m.AssistanceTicket.COMMENT,
            "service_id": ticket_service_db.service_id,
            'comment': 'Boleta fue creada manualmente sin venta. Por favor validar la cobertura de esta gestión.'
        }
        assistance_ticket_svc.create_new_assistance_ticket(data_ticket_sale)
    print("HOLAAAA VIENEEEEE EL ASSISTANCE CAR")
    print(first_ticket)
    print(first_ticket.get('car_of_assistance'))
    # Creacion y update de assistance car sale
    if "car_of_assistance" in first_ticket:
        try:
            from app.svc.assistancesale import create_car, create_car_color

            car_object = first_ticket.get('car_of_assistance')
            extra_data_car = {}
            extra_data_car['model'] = car_object['model_description']
            extra_data_car['brand'] = car_object['brand_description']
            extra_data_car['car_model_id'] = None
            extra_data_car['color'] = car_object['color_description']
            extra_data_car['car_color'] = None

            create_car(extra_data_car, extra_data_car)
            create_car_color(extra_data_car, extra_data_car)
            first_ticket.get('car_of_assistance')['car_model_id'] = extra_data_car['car_model_id']
            first_ticket.get('car_of_assistance')['car_color'] = extra_data_car['car_color']

        except Exception as e:
            print(str(traceback.format_exc()))
            pass

        if first_ticket.get('car_of_assistance').get("id"):
            print("Voy a hacerle un update al carro")
            assistance_ticket_svc.update_car_assistance(first_ticket.get('car_of_assistance'))
        elif first_ticket.get('car_of_assistance').get("car_plate"):
            print("Voy a crear un nuevo carro")
            assistance_ticket_svc.add_car_assistance( data.get('assistance_sale_id'), first_ticket.get('car_of_assistance'))


    return assistance_case, ticket_service


def validate_sale(sale_id, member_id, plan_id):
    """
        Validate if the sale of a case is valid. Validate that the member is
        the member of the sale or a dependent. Validate that the sale has the
        plan of the case.
        @param sale_id int the id of the sale
        @return string the error description
    """
    if not sale_id:
        return None
    
    # Validate the sale
    sale = db.session.query(m.AssistanceSale).filter_by(id=sale_id).first()

    if not sale:
        return 'Invalid sale'

    if sale.assistance_plan_id != plan_id:
        return 'Sale should have the plan of the case'
    
    # Check that the member if the member of the sale
    # Or a dependent of the sale
    if sale.member_id != member_id:
        # It has to be a dependent
        dependent = db.session.execute(db.select(m.AssistanceSaleDependent).where(
            m.AssistanceSaleDependent.member_id == member_id,
            m.AssistanceSaleDependent.status == m.AssistanceSaleDependent.STATUS_ACTIVE,
            m.AssistanceSaleDependent.assistance_sale_id == sale_id
        )).scalar()
        
        if not dependent:
            return 'Member is not part of the sale'

    return None

def validate_creation_assistance_case(
    create_connection_ticket, assistance_sale_id=None, service_id=None, assistance_plan_id=None, member_id=None):

    try:

        # Apply rules for tickets
        if not create_connection_ticket:
            sale = None
            if assistance_sale_id:
                sale = db.session.get(m.AssistanceSale, assistance_sale_id)

            if sale:
                # Need the plan service to apply rules
                plan_service = db.session.execute(db.select(m.AssistancePlanService).where(
                    m.AssistancePlanService.plan_id == assistance_plan_id,
                        m.AssistancePlanService.service_id == service_id
                )).scalar()
                print('///////////assistance_plan_id: ', assistance_plan_id)
                print('///////////service_id: ', service_id)
                # Can't assign a service if the plan doesn't have the service
                if not plan_service:
                    # raise errors.not_found_error
                    raise Exception("This plan has no assigned service.")

                # Check if the service has waiting time
                if plan_service.waiting_period:
                    not_on_waiting_period = validate_waiting_period(
                            plan_service.waiting_period, sale.date_effective,
                            country_svc.get_offset(sale.country)
                        )
                    if not not_on_waiting_period:
                        # If it is on waiting period
                        # raise errors.ApiError(
                        #     "Service unavailbe",
                        #     400
                        # )
                        raise Exception("This plan is in a waiting period, the assistance case cannot be created.")

                # Count services and check if the member can use it
                if plan_service.max_assistance_period:
                    # Get period to get the events from
                    from_date = None
                    current_time = datetime.now()
                    if plan_service.max_assistance_period \
                        == m.AssistancePlanService.ANNUAL_PERIOD:
                        # Use the current year as period
                        try:
                            compare_date = date(date.today().year, sale.date_effective.month, sale.date_effective.day)
                        except Exception as e:
                            print("Error compare date plan service max assistance period", str(e))
                            weekday, last_day_of_month = calendar.monthrange(date.today().year, sale.date_effective.month)
                            compare_date = date(date.today().year, sale.date_effective.month, last_day_of_month)

                        if compare_date <= current_time.date():
                            from_date = compare_date
                        else:
                            from_date = date(date.today().year - 1, sale.date_effective.month, sale.date_effective.day)
                    elif plan_service.max_assistance_period \
                        == m.AssistancePlanService.MONTHLY_PERIOD:
                        # Use current month as period
                        try:
                            compare_date = date(date.today().year, date.today().month, sale.date_effective.day)
                        except Exception as e:
                            print("Error compare date plan service monthly period", str(e))
                            weekday, last_day_of_month = calendar.monthrange(date.today().year, date.today().month)
                            compare_date = date(date.today().year, date.today().month, last_day_of_month)

                        if compare_date <= current_time.date():
                            from_date = compare_date
                        else:
                            month = date.today().month - 1
                            year = date.today().year
                            if month == 0:
                                month = 12
                                year = year -1
                            try:
                                from_date = date(year, month, sale.date_effective.day)
                            except Exception as e:
                                print("Error compare date plan service monthly period 2", str(e))
                                wd, ldom = calendar.monthrange(year, month)
                                from_date = date(year, month, ldom)

                    if from_date:
                        print('From_date: {}'.format(from_date.strftime("%d/%m/%Y, %H:%M:%S")))

                    else:
                        print("FROM_DATE NOT FOUND")

                    # Check if the member of the case is dependent or holder
                    if member_id == sale.member_id \
                        and plan_service.max_assistance != None:
                        # Holder
                        # Count services in the period of time
                        services_count = count_valid_services_by_member_service_sale(
                                [member_id], service_id, sale.id,
                                date_from=from_date
                            )
                        print('service count: ' + str(services_count))

                        if services_count >= plan_service.max_assistance:
                            raise errors.ApiError(
                                "Max events reached",
                                400
                            )

                    elif member_id != sale.member_id \
                        and plan_service.max_assistance_dependents != None:
                        # Should be dependent of sale
                        member_ids = []

                        sale_dependents = db.session.execute(db.select(m.AssistanceSaleDependent).where(
                            m.AssistanceSaleDependent.assistance_sale_id == sale.id,
                            m.AssistanceSaleDependent.status == m.AssistanceSaleDependent.STATUS_ACTIVE
                        )).scalars().all()

                        for sale_dependent in sale_dependents:
                            member_ids.append(sale_dependent.member_id)

                        # Check that the member is part of the sale
                        if member_id not in member_ids:
                            # raise errors.ApiError(
                            #     "Member is not part of the sale",
                            #     400
                            # )
                            raise Exception("This member is not part of the initial sale.")

                        services_count = count_valid_services_by_member_service_sale(
                                member_ids, service_id, sale.id,
                                date_from=from_date
                            )
                        print('service count: ' + str(services_count))

                        if services_count \
                            >= plan_service.max_assistance_dependents:
                            # raise errors.ApiError(
                            #     "Max events for dependents reached",
                            #     400
                            # )
                            raise Exception("The maximum number of events for Dependents has been reached.")

        return True, ""

    except Exception as e:
        print(str(traceback.format_exc()))
        print("error validate creation assistance case", e)
        return False, str(e)

def validate_waiting_period (waiting_period, date_effective, offset):
    """
        Validate the plan service waiting period for a sale and service
        @param waiting_period int the waiting period of the plan service
        @param date_effective datetime the date effective of the sale
        @param offset int the time offset of the country of the sale
        @return boolean if the service is possible or not.
        True is a valid service, it is not on waiting period.
        False is not a valid service, it is on waiting period
    """

    # Check if the service has waiting time
    if not waiting_period:
        return True

    effective_service_date = date_effective \
        + relativedelta(months=+waiting_period)

    now_transformed = datetime.now() + \
        relativedelta(hours=offset)

    if effective_service_date > now_transformed:
        return False

    return True

def close_tickets(case_id, close= False):
    """
        Create the close ticket if necessary
        @param case_id int case to check tickets for
    """

    tickets = db.session.query(m.AssistanceTicket) \
        .filter(m.AssistanceTicket.case_id == case_id) \
        .all()

    # Get the ids of the services that need to be closed
    close_services = get_close_tickets_info(tickets)
    autoclose_tickets(close_services, case_id, close)

def get_close_tickets_info(tickets):
    # Look for services that haven't been closed
    serviceIds = []
    caseId = None
    closedServiceIds = []
    for ticket in tickets:
        # Assign once the case id, they should all have the same case id
        if caseId == None:
            caseId = ticket.case_id

        serviceId = ticket.service_id
        if serviceId not in serviceIds:
            # Add to all services ids array
            serviceIds.append(ticket.service_id)

        if ticket.ticket_type == 5:
            # Add to closed ones
            closedServiceIds.append(ticket.service_id)

    # From all the services remove the services that are already closed
    openServices = [item for item in serviceIds if item not in closedServiceIds]

    # Return the services that need closing
    return openServices


def autoclose_tickets(serviceIds, caseId, close= False):
    """TODO: Docstring for autoclose_tickets.

    :returns: TODO

    """
    for serviceId in serviceIds:
        # Check if this service for this case is already closed
        closed_ticket = db.session.query(m.AssistanceTicket) \
            .filter(
                m.AssistanceTicket.case_id == caseId, \
                m.AssistanceTicket.service_id == serviceId, \
                m.AssistanceTicket.ticket_type == m.AssistanceTicket.CLOSED
            ) \
            .first()

        canceled = db.session.query(m.AssistanceTicket) \
            .filter(
                m.AssistanceTicket.case_id == caseId, 
                m.AssistanceTicket.service_id == serviceId,
                m.AssistanceTicket.ticket_type.in_([m.AssistanceTicket.CANCELED_BY_SUPERVISOR,
                m.AssistanceTicket.CANCELED_BY_CLIENT,
                m.AssistanceTicket.CANCELED_SERVICE_BY_REIMBURSEMENT,
                m.AssistanceTicket.CANCELED_BY_PROVIDER,
                m.AssistanceTicket.CANCELED_BY_CLIENT_WITHOUT_COST])
            ).first()

        if not closed_ticket:
            create_ticket = m.AssistanceTicket(
                case_id=caseId,
                user_id=1802866, # QUEMADO
                service_id=serviceId,
                ticket_type=m.AssistanceTicket.CLOSED,
                datetime = datetime.utcnow()
            )

            if(close):
                last_ticket = db.session.query(m.AssistanceTicket) \
                    .filter(
                        m.AssistanceTicket.case_id == caseId,
                    ) \
                    .order_by(-m.AssistanceTicket.id) \
                    .first()
                create_ticket.provider_id = last_ticket.provider_id
                create_ticket.provider_site_id = last_ticket.provider_site_id
                create_ticket.coverage_id = last_ticket.coverage_id
                create_ticket.latitude = last_ticket.latitude
                create_ticket.longitude = last_ticket.longitude
                create_ticket.provider_status = last_ticket.provider_status
                create_ticket.assistance_provider_user_id = last_ticket.assistance_provider_user_id
                
            db.session.add(create_ticket)
            db.session.flush()

            if not canceled and serviceId != 362:

                print("*********************enviar nps global************************")
                service = db.session.query(m.AssistanceService).get(serviceId)
                case = db.session.query(m.AssistanceCase).get(caseId)
                member = db.session.query(m.Member).get(case.member_id)
                country = db.session.query(m.Country).get(case.country_id)

                print("servicio")
                print(service.name)
                print("caso")
                print(case.id)
                print("correo")
                print(member.email)
                print("pais")
                print(country.name)
                print("survey status")
                print(case.rating_status)

                if(case.rating_status == 0):
                    print("si enviar correo")

                    if country.locale.startswith("es"):
                        print("español")
                        subject = "ASI Asistencia Internacional ¿Cómo te atendimos? Tu opinión en 2 minutos"
                        email_body = """<!DOCTYPE html>
<!-- saved from url=(1394)https://00f74ba44b3a4aeacd11ada8afbb7e5c0fbb6dd0c8-apidata.googleusercontent.com/download/storage/v1/b/apolo11-prod.appspot.com/o/s2_documents%2Fasys_travel%2FAsys_travel_condicionado.html?jk=AFshE3VlxWCDoeZOQZC7-J-2lNjP92b47HqSqpb_pq3n4NEQpUNOAbzDSpMW3hCilrnW1T_jl5yLsR0i9qZOEzFg4vVzTPJiRBK9_VWWoASSjhcTaiy6Yn212hIYZzT6RGdkiBskbbdcT2UI9QnUnOA33djkjyRvDQmGF1Jui4MVocAjqmTnJsbStU-qQXXebQB1WYmuN0mUV2wPp_63uIDO2W1qCwj2GGZkM3NHbLOuM5MyPvXki6toHy67GvByAlMBrJHpobYhe3jUW5MQTQ6h_hWiRTYqDuU8AioDhofnR65ku_EAU-B_e0Cwyf_PW9oTvnfSeeY6jiTora14I9GVR-YyjN3_J58JbSRH_Zg8RPjkvHEasqfNHJKIMK_HnZCYqBuVcBa-nvHwU18bjogB_TkvAPgntNpf-Zf6WS_me93yWMmmKb89Tl21MWw51uPVxW6jweSYaRe7O-EdHTXel30-dnWXhUtBeqpXpkPO4P14PNqKiH1LAY0yMmdKmmmEVQdA2SSvJY9bo_n4oKo3cegzWwQfwCMa2P52vxAVE1jYs6_cgpywmy8UOmuZwnGjNUvSPul5cjt_Od_i1tPx7ip05_Oh95W__9sR3fqSk0diuRS52CRFQy41xS9bQfrwCPYdIqxZ-TuvdakCWCZ8i86k4SZRqmrVYbDGkueiXrAhAqTAVgtYStqdDvZ6uDHjPF2GwVxgzITalSJJXUDnyqqLpGTaGuzznJ_e4x4MRaO3cajMrGyFRt2EWiCLBm7Mq3BQ7pfvESvH5H8541OSU2CP2C0N8x1f99h6esPR5bR13Cruc9kLgz4pMrMH3587Q1LL-NC_cEJ-vdvkYi4A21WW9oT6odKDa4yS1qSXyW5pNHjQgaeheP3zLjM1GZQNLiYHArTpPUx-4ovEoJD9_4bUb3ZiiyKc-Z3JTOHAVaI0-HQoDuXH4rIq2mC7YWZoxq-H043T_itUVyho_RqI4TkIlwQUfJ5przte7Luc1ZbxVnfHbJzOaGYkWjj9hcn93Epb6foJzMryIRfLtwf-ufrIVTP4H2-seHel5OcE5eKhaFfjAf1mRyS8eVXvT6MNsus4GuS0iOYHYPuM2xUytA7L0E9ay0qTyN2xcvfsqQMhADgR-5YRHuHelMD2kRPX1rLl9_U822CR0thqrT6WG_ivucwo0YJQKQ&isca=1 -->
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><script type="module" src="chrome-extension://jdkknkkbebbapilgoeccciglkfbmbnfm/hook.js"></script><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
      <!--[if gte mso 15]>
      <xml>
         <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
         </o:OfficeDocumentSettings>
      </xml>
      <![endif]-->
      
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>*|MC:SUBJECT|*</title>
      <link rel="preconnect" href="https://fonts.googleapis.com/">
      <link rel="preconnect" href="https://fonts.gstatic.com/" crossorigin="">
      <link href="./__MC_SUBJECT___files/css2" rel="stylesheet">
      <!--<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=DM+Sans:400,400i,700,700i,900,900i|Recursive:400,400i,700,700i,900,900i"/>-->
      <link rel="stylesheet" href="./__MC_SUBJECT___files/bootstrap.min.css">
      <link rel="stylesheet" href="./__MC_SUBJECT___files/font-awesome.min.css">
      <style> img{{-ms-interpolation-mode:bicubic;}} table, td{{mso-table-lspace:0pt; mso-table-rspace:0pt;}} .mceStandardButton, .mceStandardButton td, .mceStandardButton td a{{mso-hide:all !important;}} p, a, li, td, blockquote{{mso-line-height-rule:exactly;}} p, a, li, td, body, table, blockquote{{-ms-text-size-adjust:100%; -webkit-text-size-adjust:100%;}} @media only screen and (max-width: 480px){{ body, table, td, p, a, li, blockquote{{-webkit-text-size-adjust:none !important;}} }} .mcnPreviewText{{display: none !important;}} .bodyCell{{margin:0 auto; padding:0; width:100%;}} .ExternalClass, .ExternalClass p, .ExternalClass td, .ExternalClass div, .ExternalClass span, .ExternalClass font{{line-height:100%;}} .ReadMsgBody{{width:100%;}} .ExternalClass{{width:100%;}} a[x-apple-data-detectors]{{color:inherit !important; text-decoration:none !important; font-size:inherit !important; font-family:inherit !important; font-weight:inherit !important; line-height:inherit !important;}} body {{ height: 100%; margin: 0px; padding: 0px; width: 100%; background: rgb(255, 255, 255); }}p {{ margin: 0px; padding: 0px; }}table {{ border-collapse: collapse; }}td, p, a {{ word-break: break-word; }}h1, h2, h3, h4, h5, h6 {{ display: block; margin: 0px; padding: 0px; }}img, a img {{ border: 0px; height: auto; outline: none; text-decoration: none; }}@media only screen and (max-width: 480px) {{body {{ width: 100% !important; min-width: 100% !important; }}colgroup {{ display: none; }}img {{ height: auto !important; }}.mceColumn {{ display: block !important; width: 100% !important; }}#mceColumnContainer {{ padding-right: 12px !important; padding-left: 12px !important; }}.mceText, .mceText p {{ font-size: 16px !important; line-height: 150% !important; }}h1 {{ font-size: 36px !important; line-height: 125% !important; }}}} body {{ background-color: rgb(255, 255, 255); }}.mceText h1, .mceText h2, .mceText h3, .mceText h4 {{ font-family: "Helvetica Neue", Helvetica, Arial, Verdana, sans-serif; }}.mceText, .mceLabel {{ font-family: "Helvetica Neue", Helvetica, Arial, Verdana, sans-serif; }}.mceText h1, .mceText h2, .mceText h3, .mceText h4 {{ color: rgb(0, 0, 0); }}.mceText, .mceLabel {{ color: rgb(0, 0, 0); }}.mceText a {{ color: rgb(0, 0, 0); }}.mceSpacing-12 label {{ margin-bottom: 12px; }}.mceSpacing-12 input {{ margin-bottom: 12px; }}.mceSpacing-12 .mceInput + .mceErrorMessage {{ margin-top: -6px; }}.mceSpacing-24 h1 {{ margin-bottom: 24px; }}.mceSpacing-24 h1:last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 p {{ margin-bottom: 24px; }}.mceSpacing-24 p:last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 label {{ margin-bottom: 24px; }}.mceSpacing-24 input {{ margin-bottom: 24px; }}.mceSpacing-24 .last-child {{ margin-bottom: 0px; }}.mceSpacing-24 .mceInput + .mceErrorMessage {{ margin-top: -12px; }}.mceInput {{ background-color: transparent; border: 2px solid rgb(208, 208, 208); width: 60%; color: rgb(77, 77, 77); display: block; }}.mceInput[type="radio"], .mceInput[type="checkbox"] {{ float: left; margin-right: 12px; display: inline; width: auto !important; }}.mceLabel > .mceInput {{ margin-bottom: 0px; margin-top: 2px; }}.mceLabel {{ display: block; }}.mceText h1 {{ font-size: 31.248px; font-weight: 700; }} @media only screen and (max-width: 480px) {{}} @media only screen and (min-width: 481px) and (max-width: 768px) {{}}</style>
   </head>
   <body data-new-gr-c-s-check-loaded="14.1052.0" data-gr-ext-installed="" cz-shortcut-listen="true">
      <!--*|IF:MC_PREVIEW_TEXT|*-->
      <!--[if !gte mso 9]><!----><span class="mcnPreviewText" style="display:none; font-size:0px; line-height:0px; max-height:0px; max-width:0px; opacity:0; overflow:hidden; visibility:hidden; mso-hide:all;">Disfruta de la experiencia.  Te damos la bienvenida al programa de Asistencia de Viajero, con el respaldo de Muvit. Nos emociona emprender este viaje contigo, dándote un respaldo de calidad.</span><!--<![endif]-->
      <!--*|END:IF|*-->
      <div class="es-wrapper-color">
        <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0">
            <tbody>
                <tr>
                    <td class="esd-email-paddings" valign="top">       
                        <table class="es-content" cellspacing="0" cellpadding="0" align="center">
                            <tbody>
                                <tr>
                                    <td class="esd-stripe" align="center" bgcolor="#ffffff" style="background-color: #ffffff;">
                                        <table class="es-content-body" width="600" cellspacing="0" cellpadding="0" align="center" style="background-color: transparent;">
                                            <tbody>
                                                <tr>
                                                    <td class="esd-structure" align="left">
                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td class="esd-container-frame" width="600" valign="top" align="center">
                                                                        <table width="100%" cellspacing="0" cellpadding="0">
                                                                            <tbody>
                                                                     
                                                                                <tr>
                                            <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                <br>                                                
                                                
                                               
                                               
                                           </td>
                                          </tr>
                                                                                <tr>
                                                                                    <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                                                      
                                                                                      <p style="color: rgb(158, 161, 162 ); font-size: xx-large;">Esperamos que la experiencia con la asistencia de <strong style="color: rgb(91, 196, 219);"> """+str(service.name)+""" </strong> 
                                                                                       le haya sido satisfactoria y util.  </p>
                                                                                    </td>
                                                                                </tr>
                                                                               <tr>
                                            <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                <br> <br>
                                                
                                                
                                               
                                               
                                           </td>
                                          </tr>
                                                                                <tr>
                                                                                   <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                                                      
                                                                                      <p style="color: rgb(158, 161, 162 ); font-size: xx-large;">Para nosotros es muy importante su opinión, por favor ayúdenos a lograrlo contestando las siguientes preguntas:   </p>
                                                                                    </td>
                                                                                </tr>
<br> <br>
                                                                                <tr>
                                                                                  <br> <br>
                                            <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                
                                                <strong style="color: rgb(158, 161, 162 ); font-size: xx-large;">
                                                ¿Qué tan probable es que recomiende nuestro servicio de asistencia a sus familiares y amigos?
                                               </strong>
                                               
                                           </td>
                                          </tr>
                                                               
                                                                                <tr>
                                            <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                <br> <br>
                                                
                                                
                                               
                                               
                                           </td>
                                          </tr>
                                          <tr>
                                           <td align="center" class="esd-block-banner" style="position: relative; background-color: white; border-radius: 15px" esdev-config="h1">
                                                <br> <br>
                                                <table cellpadding="0" cellspacing="0" width="100%" class="es-menu" width="95%" height="87%" align="center" style="background: url( https://doctor-dev.tdasistencia.com/assets/images/teledoctormail/background.png) top center ; background-size:100% 100%; empty-cells: hide; border-collapse: separate; border-spacing: 5px;" >
                                                                                        
                                                                                            <tbody>
                                                                                                <tr class="images" >
                                                                                                  <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=0&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ ' >
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/0.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=1&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/1.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=2&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/2.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=3&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/3.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=4&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/4.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=5&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ ' >
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/5.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=6&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/6.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=7&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/7.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=8&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/8.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=9&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ '>
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/9.svg" >
                                                                                                    </td>
                                                                                                    <td>
                                                                                                      <a target="_blank" href='"""+config.SYSTEM_URL+"""/public/survey?score=10&service_id="""+str(serviceId)+"""&case_id="""+str(caseId)+"""&category_id="""+str(service.category_id)+"""&c="""+str(5)+ """ ' >
                                                                                                      <img style="width:40px; height:40px" src="https://storage.googleapis.com/apolo11-prod.appspot.com/surveys/10.svg" >
                                                                                                    </td>
                                                                                                
                                                                                                    
                                                                                                   
                                                                                                </tr>
                                                                                            </tbody>
                                                                                        </table>
                                                
                                           </td>
                                            
                                        
                                            
                                          </tr>
                                          
                                                                                
                                                                               
                                                                               
                                                                      
                                                                                
                                                                                               
                                                                                <tr>
                                            <td align="center" class="esd-block-banner" style="position: relative;" esdev-config="h1">
                                                <br> <br>
                                                
                                                
                                               
                                               
                                           </td>
                                          </tr>
                                                                                
                                                                                
                                                                                  
                                                                                
                                                                            
                                                                            
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                        <div style="margin-top: 15px; color: rgb(158, 161, 162 ); font-size: large; " ><span style="float:right;">Definitivamente <br>Recomendaría</span> Definitivamente <br>No Recomendaría</div>
                                                    </td>
                                                </tr>
                                                
  
                                                                                     
               
                        
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
   
</body><grammarly-desktop-integration data-grammarly-shadow-root="true"></grammarly-desktop-integration></html>
"""
                    elif country.locale.startswith("en"):
                        print("ingles")
                
                    customSender = 'Asistencia Internacional <no-replay@asistenciainternacional.com>'
                    customDomain = config.MAILGUN_DOMAIN_ASISTENCIA_INTERNACIONAL
                    sponsor_name = 'Asistencia Internacional'

                

                    #try:
                    #    rsp = email_svc.send_email(
                    #        case.email,
                    #        subject,
                    #        email_body,
                    #        #attachments=files,
                    #        attachments='',
                    #        sender=customSender,
                    #        domain=customDomain,
                    #        api_key=config.MAILGUN_API_KEY
                    #)
                    #    print(rsp)
                    #except Exception as e:
                    #    print(str(e))
                else:
                    print("no enviar ya esta contesado")
            else:
                print("no enviar esta cancelado")