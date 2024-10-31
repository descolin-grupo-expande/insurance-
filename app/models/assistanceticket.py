from app.extensions import db 

class AssistanceTicket(db.Model):
    """Docstring for AssistanceTicket.
    ticket_type:
        1=Assign Service
        2=Assign Provider
        3=Notify Selected Provider
        4=Provider Arrived
        5=Closed
        6=Canceled by Supervisor
        7=Canceled by Client
        8=Canceled by Provider
        9=Comment
        10=Canceled by Client, Without Cost
        11=Programmed
        12=Connection
        13=Canceled by Coverage
        14=Exception
        15=Reimburse
        16=NOTIFY_TO_CUSTOMER
        17=ASSIGN_UNASSIGN_USER
        18=DIDI
        19=LINKDIDI 
        22=coutesy_assistance
        23=canceled_service_by_reimbursement
        24= reassign provider
        30=Recordination
    car_color:
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

    car_size:
        1=Pequeno
        2=Mediano
        3=Grande
    """
    # ticket types
    ASSIGN_SERVICE = 1
    ASSIGN_PROVIDER = 2
    NOTIFY_SELECTED_PROVIDER = 3
    PROVIDER_ARRIVED = 4
    CLOSED = 5
    CANCELED_BY_SUPERVISOR = 6
    CANCELED_BY_CLIENT = 7
    CANCELED_BY_PROVIDER = 8
    COMMENT = 9
    CANCELED_BY_CLIENT_WITHOUT_COST = 10
    PROGRAMMED = 11
    CONNECTION = 12
    CANCELED_BY_COVERAGE = 13
    EXCEPTION = 14
    REIMBURSE = 15
    NOTIFY_TO_CUSTOMER = 16
    ASSIGN_UNASSIGN_USER = 17
    DIDI = 18
    LINKDIDI = 19
    COURTESY_ASSISTANCE = 22 
    CANCELED_SERVICE_BY_REIMBURSEMENT = 23
    RECORDINATION = 30

    COMMUNICATION_PHONE = 1
    COMMUNICATION_APP = 2
    COMMUNICATION_CHAT = 3
    COMMUNICATION_WHATSAPP = 4
    COMMUNICATION_EMAIL = 5
    COMMUNICATION_FACE2FACE = 6

    PROVIDER_STATUS_WILL_GO = 1
    PROVIDER_STATUS_WONT_GO = 2
    PROVIDER_OUT_OF_NETWORK = 3

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

    # Program types
    PROGRAMAR_COORDINACION = 10
    PROGRAMAR_SEGUIMIENTO = 20
    PROGRAMAR_CONF_CITA_ENVIO_CARTA = 30

    UPDATE_SURVEYS = 45


    TYPE_OF_GASOLINE_TEXT =  {
        1: 'Magna',
        2: 'Premium',
        3: 'Diesel'
    }

    DEAD_SERVICE_TYPOLOGIES = [
        "Cancelado por falta de seguimiento de cabina",
        "Cancelado porque solvento por cuenta propia"
    ]

    DEAD_SERVICE_SUBTYPOLOGIES = [
        "No se monitoreo al proveedor",
        "No se notificó quien asiste",
        "No se realizó el enlace en tiempo",
        "No se coordinó en tiempo",

        "Resuelve antes de la llegada del proveedor",
        "Alto tiempo de contacto por parte del proveedor",
        "Alto tiempo de coordinación por disponibilidad de proveedor",

        # No acepto el traslado por medio del 911 o cruz roja	
        # Servicio atendido por 911 o cruz roja	
        # Zona roja	
        # Toque de queda	
    ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_id = db.Column(db.Integer, db.ForeignKey('assistance_case.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_.id'), index=True)
    service_id = db.Column(db.Integer, db.ForeignKey('assistance_service.id'), index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('assistance_provider.id'),  index=True)
    provider_site_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_site.id'),  index=True)
    coverage_id = db.Column(db.Integer, db.ForeignKey('assistance_provider_coverage.id'),  index=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'),  index=True)
    state_area_id = db.Column(db.Integer, db.ForeignKey('district.id'),  index=True)
    datetime = db.Column("created_time", db.DateTime)
    comment = db.Column(db.UnicodeText)
    cancelation_reason = db.Column(db.UnicodeText)
    ticket_type = db.Column(db.Integer, index=True)
    communication = db.Column(db.Integer)
    provider_status = db.Column(db.Integer)
    address_destination = db.Column(db.UnicodeText(2000))
 
    latitude = db.Column(db.DOUBLE)
    longitude = db.Column(db.DOUBLE)
    car_model_id = db.Column(db.Integer, db.ForeignKey('car_model.id'),  index=True)
    car_color = db.Column(db.Integer)
    car_size = db.Column(db.SmallInteger)
    car_year = db.Column(db.Integer)
    car_plate = db.Column(db.UnicodeText(20))
    car_serial_number = db.Column(db.UnicodeText(255))
    provider_arrival_code = db.Column(db.Integer)
    supervisor_id = db.Column(db.Integer)
    exception_type = db.Column(db.Integer)
    program_type = db.Column(db.Integer)
    program_subtype = db.Column(db.Integer)
    triage = db.Column(db.Integer)
    cancellation_reason_typology = db.Column(db.UnicodeText)
    cancellation_reason_subtypology = db.Column(db.UnicodeText)
    estimated_time_arrival = db.Column(db.Float)
    assistance_provider_user_id = db.Column(db.Integer)
    
    street_destination = db.Column(db.Text)
    suburb_destination = db.Column(db.Text)
    postal_code_destination =  db.Column(db.String(15))
    gasoline_type = db.Column(db.SmallInteger)
    liters = db.Column(db.SmallInteger)

    vehicle_reference = db.Column(db.UnicodeText(500))

    area_destination = db.Column(db.String(150))
    zone_destination = db.Column(db.Integer)

    provider_cancellation_reason = db.Column(db.SmallInteger,nullable=True)
    
    email_send_required_information = db.Column(db.String(250))

    car_model = db.relationship('CarModel')
    user = db.relationship('User')
    provider = db.relationship('AssistanceProvider')
    provider_site = db.relationship('AssistanceProviderSite')
    coverage = db.relationship('AssistanceProviderCoverage')
    case = db.relationship('AssistanceCase')
    service = db.relationship('AssistanceService')
    country_state = db.relationship('CountryState', lazy='select')
    state_district = db.relationship('StateDistrict', lazy='select')


    
    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'AssistanceTicket({})'.format(self.id)

    @staticmethod
    def get_main_types():
        return [
            AssistanceTicket.ASSIGN_SERVICE,
            AssistanceTicket.ASSIGN_PROVIDER,
            AssistanceTicket.NOTIFY_SELECTED_PROVIDER,
            AssistanceTicket.PROVIDER_ARRIVED,
            AssistanceTicket.CLOSED,
            AssistanceTicket.DIDI
        ]
    
    @staticmethod
    def get_cancel_types():
        return [
            AssistanceTicket.CANCELED_BY_SUPERVISOR,
            AssistanceTicket.CANCELED_BY_CLIENT,
            AssistanceTicket.CANCELED_SERVICE_BY_REIMBURSEMENT,
            AssistanceTicket.CANCELED_BY_PROVIDER,
            AssistanceTicket.CANCELED_BY_CLIENT_WITHOUT_COST,
            AssistanceTicket.CANCELED_BY_COVERAGE
        ]

    @staticmethod
    def get_next_step(ticket_type_step):
        if ticket_type_step == AssistanceTicket.ASSIGN_SERVICE:
            return AssistanceTicket.ASSIGN_PROVIDER
        elif ticket_type_step == AssistanceTicket.ASSIGN_PROVIDER:
            return AssistanceTicket.NOTIFY_SELECTED_PROVIDER
        elif ticket_type_step == AssistanceTicket.NOTIFY_SELECTED_PROVIDER:
            return AssistanceTicket.PROVIDER_ARRIVED
        elif ticket_type_step == AssistanceTicket.PROVIDER_ARRIVED:
            return AssistanceTicket.CLOSED
        elif ticket_type_step == AssistanceTicket.DIDI:
            return AssistanceTicket.ASSIGN_PROVIDER
        
        # By default return -1 as error
        return -1
