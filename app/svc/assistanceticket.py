from app.extensions import db
from app import models as m
from app.errors import errors
import copy
from datetime import datetime, timedelta
from threading import Thread
from app.config import config
from app.svc import notification as notification_svc
from app.svc import general as gtools
from app.utils.functions import model_get_attr, set_attributes_to_from

def create_new_assistance_ticket(data):
    """
    TODO: Create a ticket for a case
    :returns: created assistance ticket
    """

    #############################################################
    # try:
    #     print(f"new_ticket_received1 {g.current_user.id}", data)
    # except:
    #     print(f"new_ticket_received1 ", data)

    main_types = m.AssistanceTicket.get_main_types()
    cancel_types = m.AssistanceTicket.get_cancel_types()
    case_id = data.get('case_id')
    service_id = data.get('service_id')
    ticket_type = data.get('ticket_type')

    # Check that the case_id exists
    case = db.session.query(m.AssistanceCase).get(case_id)

    if not case:
        raise errors.not_found_error

    if ticket_type == m.AssistanceTicket.PROVIDER_ARRIVED:
        service = db.session.query(m.AssistanceService).get(service_id)

        if case.plan.buca_plan == 1 and service.buca_service == 1:
            return [{'status_buca': 'error', 'summary': 'Error', 'message': 'La Llegada del Proveedor se registrará desde el Portal BUCA por ser un caso de BUCA.', 'return_buca': True}]
    
    # If provider is assignable on data payload
    # update the field on case register to assign provider manually
    if data.get("provider_is_assignable"):
        setattr(case, "provider_is_assignable", True)
        db.session.flush()

    # Validate the new ticket follows rules
    # Get last Ticket to get information
    last_ticket = db.session.query(m.AssistanceTicket) \
        .filter(
            m.AssistanceTicket.case_id == case_id,
            m.AssistanceTicket.service_id == service_id,
            m.AssistanceTicket.ticket_type != m.AssistanceTicket.ASSIGN_UNASSIGN_USER,
            m.AssistanceTicket.ticket_type != m.AssistanceTicket.COMMENT,
            m.AssistanceTicket.ticket_type != m.AssistanceTicket.COURTESY_ASSISTANCE, 
        ) \
        .order_by(-m.AssistanceTicket.id) \
        .first()

    print("lastickettttttttttttttttttttttttttttttttttttttt", last_ticket)

    if ticket_type == m.AssistanceTicket.CANCELED_BY_SUPERVISOR or ticket_type == m.AssistanceTicket.CANCELED_BY_CLIENT or ticket_type == m.AssistanceTicket.CANCELED_BY_PROVIDER:
        app_case = db.session.query(m.AssistanceAppCase).filter(
            m.AssistanceAppCase.assistance_case_id == case_id,
        ).first()
        if app_case and app_case.provider_user_id is not None:
            provider = db.session.query(m.User).get(app_case.provider_user_id)

            provider_fcm = provider.fcm_token

            if provider_fcm:
                #{"title":"App asisteme","message":"Push using the Seguros Cloud ntf service to asisteme app","url":"","icon":""}
                #Field "to" must be a JSON string: ["fxcfR8ZuXCw:APA91bFPzqIEeh1zVP9cPm3m6F5_g_Kz6EaouH388_YvdbkpwLPIrarwb8z7-gn3zmRiBuO5QqSnEXpKxWekiImnmTfwmbgZfrZASvEEFVNtKw6Vjwt4XvH99MnbrSVLk2lvAZwjss35"]
                notification_data = {"title":"Nueva Asistencia","message":"Una nueva solicitud de asistencia ha sido asignada en tu cuenta.","url":"","icon":""}
                notification_svc.send_plain_notification(
                    provider_fcm,
                    notification_data,
                    "Una nueva solicitud de asistencia ha sido asignada en tu cuenta."
                )
            
    if ticket_type == m.AssistanceTicket.ASSIGN_SERVICE:
        # Can't assign twice a service
        if last_ticket:
            raise errors.ApiError(
                "Can't assign a service that already exists", 400
            )
        if(service_id == 19 or service_id == 139 or service_id ==155 or service_id == 475 or service_id == 518 or service_id == 521 or service_id == 522 or service_id == 526 or service_id == 619 or service_id == 631 or service_id == 637 or service_id == 133):
            producto = db.session.query(m.AssistanceCase).get(case_id)
            country = db.session.query(m.Country).get(producto.country_id)
            #sponsor
            sponss = db.session.execute("""select s.name  as 'name' 
            from sponsor s, assistance_case ascas, assistance assi, assistance_plan asplan, assistance_sale assale 
            where s.id=assi.sponsor_id and assi.id = ascas.assistance_id and assi.id = asplan.assistance_id and asplan.id = assale.assistance_plan_id and asplan.id = ascas.assistance_plan_id
            and assale.id = ascas.assistance_sale_id and ascas.id = '"""+str(data.get('case_id'))+"""';""")

            respuestas = []
            for spo in sponss:
                row = {
                'sponsor_name' : spo.name,
            
                }
                respuestas.append(row)

            #numbers=[42476070,42905937,51930027,58254914,42143417,47086311,55718918]
    
            if respuestas == [] :
                sponsor_ = ""
            else:
                sponsor_ = str(respuestas[0]['sponsor_name'])
            numbers = db.session.query(m.Catalog).filter(m.Catalog.grouper == "SMS_ASSISTANCE").all()
            text_sms = """
            Ingreso una solicitud de ambulancia 
            No. de Boleta: """+str(data.get('case_id'))+"""
            País: """+str(country.name)+"""
            Sponsor: """+sponsor_+"""
            Producto: """+str(producto.product.name)+""" 
            Ubicación: """+str(producto.address)+"""
            Recuerda estar pendiente
            Saludos
            """
            for msm in numbers:
                datamsm = {"phone":msm.description_es, "text": str(text_sms) ,"nickname_account_related": "asistencia"}

            # send message
   
                sms = gtools.send_sms(datamsm)

        ###################################
        # Other validations are moved to 
        # create assistancecase SVC
        ###################################

    tickets_created = []

    fromApp = data.get("fromApp")
    temp_user = data.get("user_id")

    if ticket_type in cancel_types:
        appcase = db.session.query(m.AssistanceAppCase).filter(
            m.AssistanceAppCase.assistance_case_id == case_id).first()
        if appcase:
            appcase.provider_user_id = None
    providerFinished = data.get("providerCompletedJob")
    if ticket_type == m.AssistanceTicket.COMMENT:
        appcase = db.session.query(m.AssistanceAppCase).filter(
            m.AssistanceAppCase.assistance_case_id == case_id).first()
        if appcase and providerFinished == True:
            appcase.status = m.AssistanceAppCase.STATUS_CLOSED
            db.session.flush()

    # Create the ticket object with everthing received
    main_ticket = m.AssistanceTicket(
        case_id=case_id,
        service_id=service_id,
        provider_id=data.get('provider_id'),
        provider_site_id=data.get('provider_site_id'),
        coverage_id=data.get('coverage_id'),
        user_id=temp_user,
        state_id=data.get('state_id'),
        state_area_id=data.get('state_area_id'),
        datetime=datetime.now(),
        comment=data.get('comment'),
        cancelation_reason = data.get('cancelation_reason'),
        cancellation_reason_typology = data.get('cancellation_reason_typology'),
        cancellation_reason_subtypology = data.get('cancellation_reason_subtypology'),
        ticket_type=ticket_type,
        communication=data.get('communication'),
        provider_status=data.get('provider_status'),
        address_destination=data.get('address_destination'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        car_model_id=data.get('car_model_id'),
        car_color=data.get('car_color'),
        car_size=data.get('car_size'),
        car_year=data.get('car_year'),
        car_plate=data.get('car_plate'),
        car_serial_number = data.get("car_serial_number"),
        provider_arrival_code=data.get('provider_arrival_code'),
        supervisor_id = data.get('supervisor_id'),
        
        exception_type = data.get('exception_type'),
        assistance_provider_user_id = data.get('assistance_provider_user_id'),
        triage = data.get('triage'),
        street_destination = data.get('street_destination'),
        suburb_destination = data.get('suburb_destination'),
        postal_code_destination = data.get('postal_code_destination'),
        gasoline_type = data.get('gasoline_type'),
        liters = data.get('liters'),
        vehicle_reference = data.get('vehicle_reference'),
        estimated_time_arrival = data.get("timeestimated"),
        area_destination = data.get("area_destination"),
        zone_destination = data.get("zone_destination"),

        provider_cancellation_reason = data.get("provider_cancellation_reason"),
    )
    db.session.add(main_ticket)
    
    tickets_created.append(main_ticket)

    db.session.flush()

    # Assign / Unassign operator user (Only available fromApp)
    if ticket_type == m.AssistanceTicket.ASSIGN_UNASSIGN_USER and "new_operator_id" in data:

        new_operator_id = data.get("new_operator_id")

        # if assigned user then unassign
        # if case.created_by_user_id:
        if not new_operator_id:
            # Remove notifications of old user, programmed and assigned assistance
            if case.created_by_user_id:
                notification_svc.delete_last_programmed_notifications(case.id, int(main_ticket.id), case.created_by_user_id)
                notification_svc.delete_last_assign_assistance_case_notifications(case.id, case.created_by_user_id)
            
            # Then remove user
            case.created_by_user_id = None
            db.session.flush()


        # else assign operator user
        else:
            # Only if case created_by_user_id not equal to new_operator_id
            # else recreate notifications and assign new user
            if case.created_by_user_id != new_operator_id:
                # Add notification to new user
                notifications = notification_svc.assign_assistance_app_programmed_notification(
                    case.id, int(main_ticket.id), temp_user, new_operator_id
                )


                try:
                    Thread(
                        target=notification_svc.send_post_notification_for_update_mailbox,
                        args=[new_operator_id]
                    ).start()
                
                    
                except Exception as e:
                    print(e)
                    pass

                # Notification for update mailbox
                #notification_svc.send_notification_for_update_mailbox(new_operator_id)

                # Add notification to assign assistance case to user
                # Before delete last assign assistance case notifications of old user
                if case.created_by_user_id:
                    notification_svc.delete_last_assign_assistance_case_notifications(case.id, case.created_by_user_id)

                notifications2 = notification_svc.create_assign_assistance_case_app_notification(
                    case.id, new_operator_id
                )

                case.created_by_user_id = new_operator_id
                db.session.flush()


    # Assign / Unassign dispatcher user
    if ticket_type == m.AssistanceTicket.ASSIGN_UNASSIGN_USER and "new_user_id" in data:

        new_user_id = data.get("new_user_id")

        # Default type is assignated case, if fromApp, type is Assistance app notification
        custom_type = m.Notification.TYPE_ASSISTANCE_TICKET_APP_CREATED_PROGRAMMED
        if fromApp:
            custom_type = m.Notification.TYPE_ASSISTANCE_TICKET_APP_CREATED

        # if assigned user then unassign
        # if case.user_id:
        if not new_user_id:
            # Remove notifications of old user, programmed and assigned assistance
            notification_svc.delete_last_programmed_notifications(case.id, int(main_ticket.id), case.user_id, custom_type)
            notification_svc.delete_last_assign_assistance_case_notifications(case.id, case.user_id)
            
            # Then remove user
            case.user_id = None
            db.session.flush()


        # else assign user
        else:
            # Only if case user_id not equal to new_user_id
            # else recreate notifications and assign new user
            if case.user_id != new_user_id:
                # Add notification to new user
                notifications = notification_svc.assign_assistance_app_programmed_notification(
                    case.id, int(main_ticket.id), temp_user, new_user_id, custom_type
                )

                # Add notification to assign assistance case to user
                # Before delete last assign assistance case notifications of old user
                if case.user_id:
                    notification_svc.delete_last_assign_assistance_case_notifications(case.id, case.user_id, custom_type)

                notifications2 = notification_svc.create_assign_assistance_case_app_notification(
                    case.id, new_user_id, custom_type
                )

                case.user_id = new_user_id
                db.session.flush()
    
    if main_ticket.ticket_type == m.AssistanceTicket.ASSIGN_SERVICE:

        last_ticket = main_ticket

    if main_ticket.ticket_type == m.AssistanceTicket.ASSIGN_UNASSIGN_USER and not last_ticket:
        last_ticket = main_ticket

    columns_use_from_last = [] 
    # Set the values of the last ticket on the correct columns
    main_ticket = set_attributes_to_from(
        main_ticket, last_ticket, columns_use_from_last
    )
    db.session.flush()

    # On assign service ticket can create programmed and connection ticket
    # For these types of tickets only set comment
    columns_use_from_last = model_get_attr(
        m.AssistanceTicket,
        exclude=[
            'id', 'case_id', 'service_id', 'user_id', 'datetime', 'program_type','triage','program_subtype',
            'comment', 'ticket_type','cancelation_reason', 'cancellation_reason_typology', 'cancellation_reason_subtypology', 'estimated_time_arrival', 'provider_cancellation_reason'
        ]
    )

    # Set Term Hour to ticket
    if data.get("custom_datetime"):
        main_ticket.datetime = data.get("custom_datetime")
        db.session.flush()
      
    print('ESTOS SON LOS TICKETS CREADOS', tickets_created)
    return tickets_created


def get_next_operator_id_online(service_id, client_id=None, fromApp=False):
    """
        Assign operator ready to run Round Robin algorithm to assign operator
        based on last assigned job field on User model to select assistance app operator
    """
    print("GET_NEXT_OPERATOR_ID_ONLINE, params: {}, {}, {}".format(service_id, client_id, fromApp))

    operator = None

    # Get roles by category name to assign operator
    # If this case is from app, assign it to an operator VIP
    if fromApp:
        roles = [config.ASSISTANCE_OPERATOR_VIP]
    else:
        roles = [config.OPERATOR]

    # Only if we have a member id run this thread
    if client_id:
        # Create date from date today and offset 6 hours
        now = datetime.now()
        # from_date = datetime(now.year, now.month, now.day, 6, 0, 0)
        # 24 hours max offset to assign
        from_date = now - timedelta(hours=24)

        print("NEXT_OPERATOR, MEMBER ID FROM DATE: {}".format(from_date))

        # Search assistance cases from date today and the client_id
        # If have any case, return self operator for all cases for client
        cases_client = db.session.query(m.AssistanceCase).filter(
            m.AssistanceCase.member_id == client_id,
            m.AssistanceCase.created_by_user_id != None,
            m.AssistanceCase.date_start >= from_date
        ).order_by(m.AssistanceCase.id).limit(2)

        print("NEXT_OPERATOR, CASES OF MEMBER: {}".format(cases_client.count()))

        # Verify if count is grether than 1 because
        # the number 1 is self created assistance case
        if cases_client.count() >= 1:
            case_oldest = cases_client.first()
            oldest_operator_id = case_oldest.created_by_user_id

            print("NEXT_OPERATOR, CASE OLDEST ID: {}, USER ID: {}".format(case_oldest.id, oldest_operator_id))

            # Get self operator id if status online
            if oldest_operator_id:
                # operator = db.session.query(m.User).filter(
                #     m.User.id == oldest_operator_id,
                #     m.User.connection_status.in_(m.User.STATUS_ONLINE, m.User.STATUS_OFFLINE_AVAILABLE)
                # ).first()

                operator = db.session.query(m.User) \
                    .join(m.UserRol, m.User.id == m.UserRol.user_id) \
                    .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
                    .filter(
                        m.User.id == oldest_operator_id,
                        m.User.status == m.User.STATUS_ACTIVE,
                        m.Rol.name.in_(roles),
                        m.User.connection_status == m.User.STATUS_ONLINE
                    ).first()

                # If operator found online, return
                if operator:
                    if operator.connection_status in [m.User.STATUS_ONLINE, m.User.STATUS_OFFLINE_AVAILABLE]:
                        # Update last assigned job to first operator in query
                        print("NEXT_OPERATOR USER {} IS ONLINE. SELECTED_OPERATOR".format(operator.id, operator.connection_status))
                        setattr(operator, "last_assigned_job", datetime.now() - timedelta(hours=6))
                        db.session.flush()
                        return operator.id, operator

                    else:
                        print("NEXT_OPERATOR USER {} IS NOT ONLINE: {}".format(operator.id, operator.connection_status))

    service = db.session.query(m.AssistanceService).get(service_id)

    # If is category attended by himself, return current user logged in
    if not fromApp and service.category.name in config.SERVICES_ATTENDED_BY_CURRENT_USER:
        operator = 26 # QUEMADO

    else:

        # Users online only
        # Operators without last assigned job first
        operators1 = db.session.query(m.User) \
            .join(m.UserRol, m.User.id == m.UserRol.user_id) \
            .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
            .filter(
                m.User.connection_status == m.User.STATUS_ONLINE,
                m.User.status == m.User.STATUS_ACTIVE,
                m.Rol.name.in_(roles),
                m.User.last_assigned_job == None
            ).all()

        # Then operators order by last assigned job if is not None
        # Ordered by datetime last_assigned_job ascendent get the oldest date first
        operators2 = db.session.query(m.User) \
            .join(m.UserRol, m.User.id == m.UserRol.user_id) \
            .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
            .filter(
                m.User.connection_status == m.User.STATUS_ONLINE,
                m.User.status == m.User.STATUS_ACTIVE,
                m.Rol.name.in_(roles),
                m.User.last_assigned_job != None
            ).order_by(m.User.last_assigned_job.asc()).all()

        # Join queries
        operators = operators1 + operators2

        ###################################################
        # USERS OFFLINE AVAILABLE
        ###################################################
        # If not operator online founded
        # Search over status offline available
        ###################################################
        if len(operators) == 0:
            # Users offline available only
            # Operators without last assigned job first
            operators1 = db.session.query(m.User) \
                .join(m.UserRol, m.User.id == m.UserRol.user_id) \
                .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
                .filter(
                    m.User.connection_status == m.User.STATUS_OFFLINE_AVAILABLE,
                    m.User.status == m.User.STATUS_ACTIVE,
                    m.Rol.name.in_(roles),
                    m.User.last_assigned_job == None
                ).all()

            # Users offline available only
            # Then operators order by last assigned job if is not None
            # Ordered by datetime last_assigned_job ascendent get the oldest date first
            operators2 = db.session.query(m.User) \
                .join(m.UserRol, m.User.id == m.UserRol.user_id) \
                .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
                .filter(
                    m.User.connection_status == m.User.STATUS_OFFLINE_AVAILABLE,
                    m.User.status == m.User.STATUS_ACTIVE,
                    m.Rol.name.in_(roles),
                    m.User.last_assigned_job != None
                ).order_by(m.User.last_assigned_job.asc()).all()

            # Join queries
            operators = operators1 + operators2

        if len(operators) > 0:
            operator = operators[0]

    if not operator:
        return None, None

    # Update last assigned job to first operator in query
    print("NEXT_OPERATOR USER {} IS ONLINE. SELECTED_OPERATOR_2".format(operator.id))
    setattr(operator, "last_assigned_job", datetime.now() - timedelta(hours=6))
    db.session.flush()

    return operator.id, operator

def get_next_dispatcher_id_online(service_id, client_id=None, fromApp=False):
    """
        Assign dispatcher ready to run Round Robin algorithm to assign dispatcher
        based on last assigned job field on User model to select assistance dispatcher
    """
    print("GET_NEXT_DISPATCHER_ID_ONLINE, params: {}, {}, {}".format(service_id, client_id, fromApp))

    dispatcher = None

    service = db.session.query(m.AssistanceService).get(service_id)

    # Get roles by category name to assign dispatcher
    if fromApp:
        roles = [config.ASSISTANCE_DISPATCHER_VIP]

    elif service.category.name in config.SERVICES_ATTENDED_TO_MEDICAL:
        roles = [config.ASSISTANCE_DISPATCHER_MEDICAL]

    elif service.category.name in config.SERVICES_ATTENDED_TO_VIAL:
        roles = [config.ASSISTANCE_DISPATCHER_VIAL]

    else:
        roles = [config.ASSISTANCE_DISPATCHER]

    # Only if we have a member id run this thread
    if client_id:
        # Create date from date today and offset 6 hours
        now = datetime.now()
        # from_date = datetime(now.year, now.month, now.day, 6, 0, 0)
        # 24 hours max offset to assign
        from_date = now - timedelta(hours=24)

        print("NEXT_DISPATCHER, MEMBER ID FROM DATE: {}".format(from_date))

        # Search assistance cases from date today and the client_id
        # If have any case, return self dispatcher for all cases for client
        cases_client = db.session.query(m.AssistanceCase).filter(
            m.AssistanceCase.member_id == client_id,
            m.AssistanceCase.user_id != None,
            m.AssistanceCase.date_start >= from_date
        ).order_by(m.AssistanceCase.id).limit(2)

        print("NEXT_DISPATCHER, CASES OF MEMBER: {}".format(cases_client.count()))

        # Verify if count is grether than 1 because
        # the number 1 is self created assistance case
        if cases_client.count() >= 1:
            case_oldest = cases_client.first()
            oldest_dispatcher_id = case_oldest.user_id

            print("NEXT_DISPATCHER, CASE OLDEST ID: {}, USER ID: {}".format(case_oldest.id, oldest_dispatcher_id))

            # Get self dispatcher id if status online
            if oldest_dispatcher_id:
                # dispatcher = db.session.query(m.User).filter(
                #     m.User.id == oldest_dispatcher_id,
                #     m.User.connection_status.in_(m.User.STATUS_ONLINE, m.User.STATUS_OFFLINE_AVAILABLE)
                # ).first()

                # dispatcher = db.session.query(m.User).filter(
                #     m.User.id == oldest_dispatcher_id,
                #     m.User.status == m.User.STATUS_ACTIVE,
                #     m.User.connection_status == m.User.STATUS_ONLINE
                # ).first()

                dispatcher = db.session.query(m.User) \
                    .join(m.UserRol, m.User.id == m.UserRol.user_id) \
                    .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
                    .filter(
                        m.User.id == oldest_dispatcher_id,
                        m.User.status == m.User.STATUS_ACTIVE,
                        m.Rol.name.in_(roles),
                        m.User.connection_status == m.User.STATUS_ONLINE
                    ).first()


                # If dispatcher found online, return
                if dispatcher:
                    if dispatcher.connection_status in [m.User.STATUS_ONLINE, m.User.STATUS_OFFLINE_AVAILABLE]:
                        # Update last assigned job to first dispatcher in query
                        print("NEXT_DISPATCHER USER {} IS ONLINE. SELECTED_DISPATCHER".format(dispatcher.id))
                        setattr(dispatcher, "last_assigned_job", datetime.now() - timedelta(hours=6))
                        db.session.flush()
                        return dispatcher.id, dispatcher

                    else:
                        print("NEXT_DISPATCHER USER {} IS NOT ONLINE: {}".format(dispatcher.id, dispatcher.connection_status))

    # If is category attended by himself, return current user logged in
    if not fromApp and service.category.name in config.SERVICES_ATTENDED_BY_CURRENT_USER:
        dispatcher = 26 # QUEMADO

    else:
        # Users online only
        # Dispatchers without last assigned job first
        dispatchers1 = db.session.query(m.User) \
            .join(m.UserRol, m.User.id == m.UserRol.user_id) \
            .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
            .filter(
                m.User.connection_status == m.User.STATUS_ONLINE,
                m.User.status == m.User.STATUS_ACTIVE,
                m.Rol.name.in_(roles),
                m.User.last_assigned_job == None
            ).all()

        # Then dispatchers order by last assigned job if is not None
        # Ordered by datetime last_assigned_job ascendent get the oldest date first
        dispatchers2 = db.session.query(m.User) \
            .join(m.UserRol, m.User.id == m.UserRol.user_id) \
            .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
            .filter(
                m.User.connection_status == m.User.STATUS_ONLINE,
                m.User.status == m.User.STATUS_ACTIVE,
                m.Rol.name.in_(roles),
                m.User.last_assigned_job != None
            ).order_by(m.User.last_assigned_job.asc()).all()

        # Join queries
        dispatchers = dispatchers1 + dispatchers2

        ###################################################
        # USERS OFFLINE AVAILABLE
        ###################################################
        # If not dispatcher online founded
        # Search over status offline available
        ###################################################
        if len(dispatchers) == 0:
            # Users offline available only
            # Dispatchers without last assigned job first
            dispatchers1 = db.session.query(m.User) \
                .join(m.UserRol, m.User.id == m.UserRol.user_id) \
                .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
                .filter(
                    m.User.connection_status == m.User.STATUS_OFFLINE_AVAILABLE,
                    m.User.status == m.User.STATUS_ACTIVE,
                    m.Rol.name.in_(roles),
                    m.User.last_assigned_job == None
                ).all()

            # Users offline available only
            # Then dispatchers order by last assigned job if is not None
            # Ordered by datetime last_assigned_job ascendent get the oldest date first
            dispatchers2 = db.session.query(m.User) \
                .join(m.UserRol, m.User.id == m.UserRol.user_id) \
                .join(m.Rol, m.UserRol.role_id == m.Rol.id) \
                .filter(
                    m.User.connection_status == m.User.STATUS_OFFLINE_AVAILABLE,
                    m.User.status == m.User.STATUS_ACTIVE,
                    m.Rol.name.in_(roles),
                    m.User.last_assigned_job != None
                ).order_by(m.User.last_assigned_job.asc()).all()

            # Join queries
            dispatchers = dispatchers1 + dispatchers2

        if len(dispatchers) > 0:
            dispatcher = dispatchers[0]

    if not dispatcher:
        return None, None

    # Update last assigned job to first dispatcher in query
    print("NEXT_DISPATCHER USER {} IS ONLINE. SELECTED_DISPATCHER_2".format(dispatcher.id))
    setattr(dispatcher, "last_assigned_job", datetime.now() - timedelta(hours=6))
    db.session.flush()

    return dispatcher.id, dispatcher

def update_car_assistance(car_of_assistance):
    print("ESTO TENGO PARA HACER EL UPDATE DEL CARRO")
    print(car_of_assistance)
    car = db.session.query(m.AssistanceSaleCar).filter(m.AssistanceSaleCar.id == car_of_assistance.get('id')).first()
    if car:
        setattr(car, "car_plate", car_of_assistance.get('car_plate'))
        setattr(car, "car_year", car_of_assistance.get('car_year'))
        setattr(car, "brand_description", car_of_assistance.get('brand_description'))
        setattr(car, "model_description", car_of_assistance.get('model_description'))
        setattr(car, "color_description", car_of_assistance.get('color_description'))
        setattr(car, "type_description", car_of_assistance.get('type_description'))
        setattr(car, "serial_number", car_of_assistance.get('serial_number'))
        setattr(car, "engine_number", car_of_assistance.get('engine_number'))
        setattr(car, "car_model_id", car_of_assistance.get('car_model_id'))
        setattr(car, "car_color", car_of_assistance.get('car_color'))
        db.session.flush()

def add_car_assistance(assistance_sale_id,car_of_assistance):
    print("ESTO TENGO PARA HACER LA CREACION DEL CARRO")
    print(car_of_assistance)
    car = m.AssistanceSaleCar(
        assistance_sale_id = assistance_sale_id,
        car_plate = car_of_assistance.get('car_plate'),
        car_year = car_of_assistance.get('car_year'),
        brand_description = car_of_assistance.get('brand_description'),
        model_description = car_of_assistance.get('model_description'),
        color_description = car_of_assistance.get('color_description'),
        type_description = car_of_assistance.get('type_description'),
        serial_number = car_of_assistance.get('serial_number'),
        engine_number = car_of_assistance.get('engine_number'),
        car_model_id = car_of_assistance.get('car_model_id'),
        car_color = car_of_assistance.get('car_color'),
        status = 1
    )
    db.session.add(car)
    db.session.flush()
    print(car)
    