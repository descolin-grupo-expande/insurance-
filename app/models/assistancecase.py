from app.extensions import db
from datetime import datetime

class AssistanceCase(db.Model):
    """Docstring for AssistanceCase.

    payment_method:
        0: Transfer
        1: Check
    is_paid:
        0: Unpaid
        1: Paid
    """

    STATUS_OPEN = 1
    STATUS_CLOSE = 2

    MEMBER_STATUS_ACTIVE = 1
    MEMBER_STATUS_PENDING = 2

    RATING_EXCELLENT = 1
    RATING_GOOD = 2
    RATING_REGULAR = 3
    RATING_BAD = 4

    EFFORT_RATING_TOO_MUCH = 1
    EFFORT_RATING_SOME = 2
    EFFORT_RATING_NORMAL = 3
    EFFORT_RATING_LITTLE = 4
    EFFORT_RATING_VERY_LITTLE = 5

    RATING_STATUS_DONT_ANSWER = 0
    RATING_STATUS_ANSWERED = 1
    RATINGS_STATUS_DOESNT_APPLY = 2

    PAYMENT_METHOD_TRANSFER = 0
    PAYMENT_METHOD_CHECK = 1

    ASSISTANCE_REPROCESS_EVALUTED = 1
    ASSISTANCE_REPROCESS_NOT_EVALUTED = 0

    STATUS_SEND_INFORMATION_GEOCERCAS = {
        "SENT_TO_GEOCERCAS_AND_PROCESSED": 1,
        "SENT_TO_GEOCERCAS_AND_NOT_PROCESSED": 2,
        "NOT_SEND_TO_GEOCERCAS": 3,
    }

    # SURVEY_GROUP_TYPES = [
    #     Group.ASSISTANCE_CASE_SURVEY,
    #     Group.ASSISTANCE_CASE_DISPATCHER_SURVEY,
    #     Group.ASSISTANCE_CASE_TELEDOCTOR_SURVEY,
    #     Group.ASSISTANCE_CASE_TELEDOCTOR_SURVEY_VIDEO,
    #     Group.ASSISTANCE_CASE_TELEDOCTOR_SURVEY_CHAT,
    #     Group.ASSISTANCE_CASE_TELEDOCTOR_SURVEY_OMT,
    #     Group.ASSISTANCE_CASE_CABIN_SURVEY,
    #     Group.ASSISTANCE_CASE_DISPATCH_SURVEY,
    #     Group.ASSISTANCE_CASE_COMPLETE_SURVEY,
    #     Group.ASSISTANCE_CASE_INFORMATION_SURVEY,
    #     Group.ASSISTANCE_CASE_CABIN_SURVEY_AMBULANCE,
    #     Group.ASSISTANCE_CASE_DISPATCH_SURVEY_AMBULANCE,
    #     Group.ASSISTANCE_CASE_COMPLETE_SURVEY_AMBULANCE,
    #     Group.EMAIL_GROUP1,
    #     Group.EMAIL_GROUP2,
    #     Group.EMAIL_GROUP3,
    #     Group.EMAIL_GROUP4,
    #     Group.EMAIL_GROUP5,
    #     Group.EMAIL_GROUP6,
    #     Group.EMAIL_GROUP7,
    #     Group.EMAIL_GROUP8,
    #     Group.EMAIL_GROUP9,
    #     Group.ASSISTANCE_CASE_TELEDOCTOR_SURVEY_OMT_Odonto,
    #     Group.ASSISTANCE_CASE_TELEDOCTOR_SURVEY_OMT_Psico,
    # ]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), index=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), index=True)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), index=True)
    state_district_id = db.Column(db.Integer, db.ForeignKey("district.id"), index=True)
    assistance_id = db.Column(db.Integer, db.ForeignKey("assistance.id"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_.id"), index=True)
    assistance_plan_id = db.Column(db.Integer, db.ForeignKey("assistance_plan.id"), index=True)
    assistance_sale_id = db.Column(db.Integer, db.ForeignKey("assistance_sale.id"), index=True)
    address = db.Column(db.UnicodeText(250))
    phone = db.Column(db.String(50))
    phone2 = db.Column(db.String(50))
    email = db.Column(db.String(100))
    country_phone_code = db.Column(db.String(10))
    latitude = db.Column(db.DOUBLE)
    longitude = db.Column(db.DOUBLE)
    member_comment = db.Column(db.Text)
    date_start = db.Column(db.DateTime, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Integer, default=STATUS_OPEN)
    contact_channel = db.Column(db.Integer)
    contact_name = db.Column(db.String(150))
    applicant_name = db.Column(db.String(150))
    member_status = db.Column(db.Integer, default=1)
    speed_rating = db.Column(db.Integer)
    phone_rating = db.Column(db.Integer)
    time_rating = db.Column(db.Integer)
    service_rating = db.Column(db.Integer)
    complaint = db.Column(db.Integer)
    effort_rating = db.Column(db.Integer)
    recommendation_rating = db.Column(db.Integer)
    rating_status = db.Column(db.Integer, default=0)
    bill_comment = db.Column(db.Text)
    payment_method = db.Column(db.SmallInteger)
    is_paid = db.Column(db.SmallInteger, default=0)
    zone = db.Column(db.Integer)
    area = db.Column(db.String(150))
    is_assistance_reprocess_evaluated = db.Column(db.SmallInteger, default=0)
    destination_latitude = db.Column(db.DOUBLE)
    destination_longitude = db.Column(db.DOUBLE)
    provider_is_assignable = db.Column(db.Boolean, default=True)

    created_by_user_id = db.Column(db.Integer, db.ForeignKey("user_.id"), index=True)
    # sds_sinister_claim_id = db.Column(db.
    #     Integer, db.ForeignKey("sds_sinister_claim.id"), index=True
    # )

    street = db.Column(db.Text)
    suburb = db.Column(db.Text)
    postal_code = db.Column(db.String(15))
    reference = db.Column(db.String(200))

    status_send_information_geocercas = db.Column(db.SmallInteger)

    customer_first_name = db.Column(db.String(500))
    customer_middle_name = db.Column(db.String(500))
    customer_last_name = db.Column(db.String(500))
    customer_last_name_2 = db.Column(db.String(500))
    business_name = db.Column(db.String(500))

    ###agrego estos nuevos campos a la tabla assistance_case
    grouping_id = db.Column(db.Integer)
    grouping_chubb = db.Column(db.String(500))
    attendance_identifier = db.Column(db.Integer)
    free_text_attendance = db.Column(db.String(500))
    apply_survey = db.Column(db.Boolean, default=True)
    apply_alerts = db.Column(db.Boolean, default=False)
    alert_mail = db.Column(db.String(150))
    item_number = db.Column(db.Integer)

    reimbursement_date = db.Column(db.DateTime)
    reimbursement_amount = db.Column(db.Numeric(precision=12, scale=2))
    case_ticket_info = db.Column(db.Text)
    procesado_sc = db.Column(db.Boolean)

    appointment_date = db.Column(db.DateTime)

    reassigned_operator_case = db.Column(db.Boolean, default=False)
    reassigned_dispatcher_case = db.Column(db.Boolean, default=False)
    reassigned_tracking_case = db.Column(db.Boolean, default=False)

    origin_country_id = db.Column(db.Integer, db.ForeignKey("country.id"), index=True)
    destination_country_id = db.Column(db.Integer, db.ForeignKey("country.id"), index=True)

    assistance_sale = db.relationship(
        "AssistanceSale", lazy="select", foreign_keys=[assistance_sale_id]
    )
    member = db.relationship("Member", lazy="select")
    created_by = db.relationship("User", lazy="select", foreign_keys=[user_id])
    created_by_user = db.relationship(
        "User", lazy="select", foreign_keys=[created_by_user_id]
    )
    country = db.relationship("Country", lazy="select",  foreign_keys=[country_id])
    product = db.relationship("Assistance", lazy="select")
    countryState = db.relationship("CountryState", lazy="select")
    stateDistrict = db.relationship("StateDistrict", lazy="select")
    plan = db.relationship("AssistancePlan", lazy="select")
    tickets = db.relationship("AssistanceTicket", overlaps="case")
    # sds_sinister_claim = db.relationship(
    #     "SdsClaim", lazy="select", foreign_keys=[sds_sinister_claim_id]
    # )

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return "AssistanceCase({})".format(self.id)

    # def toDict(self):
    #     return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    # @hybrid_property
    # def arrived_ticket(self):
    #     arrived_ticket_list = [
    #         ticket
    #         for ticket in self.tickets
    #         if ticket.ticket_type == AssistanceTicket.PROVIDER_ARRIVED
    #     ]
    #     return arrived_ticket_list[0] if len(arrived_ticket_list) > 0 else None
