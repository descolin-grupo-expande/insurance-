from app.extensions import db

class AssistancePlanService(db.Model):

    """Docstring for AssistancePlanService. """

    ANNUAL_PERIOD = 1
    MONTHLY_PERIOD = 2

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('assistance_plan.id'))
    assistance_plan_addon_id = db.Column(db.Integer, db.ForeignKey('assistance_plan_addon.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('assistance_service.id'))
    max_assistance = db.Column(db.Integer)
    max_amount = db.Column(db.Numeric(precision=12, scale=2))
    max_amount_general = db.Column(db.Numeric(precision=12, scale=2))
    participation_amount = db.Column(db.Numeric(precision=12, scale=2))
    participation_percentage = db.Column(db.Numeric(precision=12, scale=2))
    periodicity = db.Column(db.Integer)
    waiting_period = db.Column(db.Integer)
    max_assistance_period = db.Column(db.SmallInteger)
    max_assistance_dependents = db.Column(db.Integer)
    phone_number = db.Column(db.Unicode(20))
    emergency_reporting_time = db.Column(db.Integer)
    dependents_scope_coverage = db.Column(db.UnicodeText(500))
    territoriality = db.Column(db.UnicodeText(500))
    coordination_schedule = db.Column(db.UnicodeText(500))
    special_condition = db.Column(db.UnicodeText(1000))
    observations = db.Column(db.UnicodeText(500))
    family_Individual = db.Column(db.UnicodeText(500))
    max_percentage_dependent = db.Column(db.Numeric(precision=12, scale=2))
    max_percentage_holder = db.Column(db.Numeric(precision=12, scale=2))
    image_preprocedure = db.Column(db.Integer)
    image_postprocedure = db.Column(db.Integer)
    maximum_age = db.Column(db.Integer)
    # max_amount_event_national = db.Column(db.Numeric(precision=12, scale=2))
    # max_amount_event_foreign = db.Column(db.Numeric(precision=12, scale=2))
    # currency_max_amount = db.Column(db.Integer,db.ForeignKey('currency.id'))
    # currency_copago = db.Column(db.Integer,db.ForeignKey('currency.id'))
