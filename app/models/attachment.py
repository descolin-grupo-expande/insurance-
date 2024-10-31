from app.extensions import db
from datetime import datetime
from app.config import config
from app import models as m

class Attachment(db.Model):

    """Docstring for Attachment.
    attachment_type
        0=assistance_sale
        1=insurance_sale
        2=insurance_ticket
        3=insurance_product
        4=medical_provider
        5=assistance_provider


        49=assistance_files
    """

    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1

    TYPE_ASSISTANCE_SALE = 0
    TYPE_INSURANCE_SALE = 1
    TYPE_INSURANCE_TICKET = 2
    TYPE_INSURANCE_PRODUCT = 3
    TYPE_MEDICAL_PROVIDER = 4
    TYPE_ASSISTANCE_PROVIDER = 5
    TYPE_ASSISTANCE_MAIL = 6 
    TYPE_INSURANCE_ATTACHMENT = 7
    TYPE_MEDICAL_TICKET = 8
    TYPE_MEDICAL_PHARMACY_PRODUCT = 9
    TYPE_REPORT_ATTACHMENT = 10
    TYPE_CKEDITOR_IMAGE = 11
    TYPE_CAR = 12
    TYPE_TELEDOCTOR_SALE = 13
    TYPE_CRM_MAIL = 14
    TYPE_TELEDOCTOR_TICKET = 15
    TYPE_MEDICAL_PHARMACY_LOCATION_PRODUCT = 16
    TYPE_MEDICAL_PROVIDER_SERVICE_IMPORT = 17
    TYPE_MEDICAL_PROVIDER_LABORATORY_IMPORT = 18
    TYPE_MEDICAL_CONSULTATION_TICKET = 19
    TYPE_ASSISTANCE_MAIL_FILE = 20 
    TYPE_SITE_LOGO = 20
    TYPE_SITE_FAVICON = 21
    TYPE_SITE_BACKGROUND = 22
    TYPE_SITE_HEADER = 23
    TYPE_SITE_FOOTER = 24
    TYPE_FRONTING_LOGO = 26
    TYPE_MEDICAL_PROVIDER_CHILDREN = 27
    TYPE_MEDICAL_CLAIM_TICKET = 28
    TYPE_INSURANCE_CASE_CLAIM = 29
    TYPE_ASSISTANCE_REPROCESS = 30
    TYPE_MEDICAL_CLAIM_TICKET = 31
    TYPE_MEDICAL_LOCATION_PROVIDERS = 32
    TYPE_ASSISTANCE_PAYMENT_BATCH = 33
    TYPE_ASSISTANCE_CREDIX_PROSPECTS = 34
    TYPE_ASSISTANCE_PLAN_MAIL = 35
    TYPE_ASSISTANCE_PLAN_MAIL_FILE = 36
    TYPE_ASSISTANCE_PLAN_APP_FILE = 37
    TYPE_MEDICAL_AUTHORIZATION_FILE = 38
    TYPE_MEDICAL_PAYMENT_BATCH = 39
    TYPE_ASSISTANCE_PROVIDER_BILL = 40
    TYPE_ASSISTANCE_CMPG_MAIL = 41
    TYPE_ASSISTANCE_CMPG_MAIL_FILE = 42
    TYPE_PROSPECTS = 43
    TYPE_ASSISTANCE_SALE_FILE = 49
    TYPE_AUTOMATIC_LETTER = 50
    TYPE_IS_MAIL_SALE = 54
    TYPE_BUCA_MAIL = 55
    TYPE_WALLET_ASSET = 56
    TYPE_WALLET_ASSET_ICON = 57
    TYPE_WALLET_ASSET_ICON2X = 58
    TYPE_WALLET_ASSET_LOGO = 59
    TYPE_WALLET_ASSET_LOGO2X = 60
    TYPE_WALLET_ASSET_STRIP = 61
    TYPE_WALLET_ASSET_STRIP2X = 62
    TYPE_WALLET_ASSET_STRIP3X = 63
    TYPE_DIGITAL_CLAIMS = 56
    TYPE_DIGITAL_CLAIMS_EDITABLE = 57

    TYPE_MENSAJE_HACIENDA_CR = 80
    TYPE_FACTURA_HACIENDA_CR = 90
    
    #quality breach
    TYPE_FINDING = 101
    Retroa_callback = 102
    Retroalimentación = 103
    Callback = 104
    monestación_proceso_disciplinario = 105
    Foto = 106
    Correos = 107
    Finiquitos = 108
    Solicitud = 109
    Apelacion = 110
    Analisis_del_hallazgo_por_oficial_riesgo = 111
     
    TYPE_ASSISTANCE_PRODUCT = 112
    TYPE_ASSISTANCE_PLAN = 113

    TYPE_CREFISA_FORM = 96
    TYPE_SIGN_OWNER = 98
    TYPE_SIGN_DRIVER = 97
    TYPE_CREFISA_LETTER = 99
    TYPE_DICTUM = 100

    CONTENT_TYPE_BY_EXT = {
        'png': 'image/png',
        'jpg': 'image/jpg',
        'jpeg': 'image/jpeg',
        'pdf': 'application/pdf',
        'PDF': 'application/pdf',
        'html': 'text/html',
        'csv': 'text/csv',
        'msg': 'application/octet-stream',
        'xml': 'application/xml',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'wav': 'audio/wav',
        'mp3': 'audio/mpeg',
        'msg': 'application/octet-stream',
        'm4a': 'audio/mp4',
        'ogg': 'audio/ogg'
    }

    FOLDERNAME_BY_TYPE = {
        TYPE_ASSISTANCE_PROVIDER_BILL: config.ASSISTANCE_PROVIDER_BILL_ATTACHMENT_DIR,
        TYPE_MENSAJE_HACIENDA_CR: config.ASSISTANCE_PROVIDER_BILL_ATTACHMENT_DIR,
        TYPE_FACTURA_HACIENDA_CR: config.ASSISTANCE_PROVIDER_BILL_ATTACHMENT_DIR,
        TYPE_FINDING: config.TYPE_FINDING_ATTACHMENT_DIR,
        Retroa_callback: config.TYPE_FINDING_ATTACHMENT_DIR,
        Retroalimentación: config.TYPE_FINDING_ATTACHMENT_DIR,
        Callback: config.TYPE_FINDING_ATTACHMENT_DIR,
        monestación_proceso_disciplinario: config.TYPE_FINDING_ATTACHMENT_DIR,
        Foto: config.TYPE_FINDING_ATTACHMENT_DIR,
        Correos: config.TYPE_FINDING_ATTACHMENT_DIR,
        Finiquitos: config.TYPE_FINDING_ATTACHMENT_DIR,
        Solicitud: config.TYPE_FINDING_ATTACHMENT_DIR,
        Apelacion: config.TYPE_FINDING_ATTACHMENT_DIR,
        Analisis_del_hallazgo_por_oficial_riesgo: config.TYPE_FINDING_ATTACHMENT_DIR,
        TYPE_WALLET_ASSET: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_ICON: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_ICON2X: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_LOGO: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_LOGO2X: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_STRIP: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_STRIP2X: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_WALLET_ASSET_STRIP3X: config.ASSISTANCE_WALLET_ASSETS_DIR,
        TYPE_ASSISTANCE_PRODUCT: config.ASSISTANCE_PRODUCT_ATTACHMENT_DIR,
        TYPE_ASSISTANCE_PLAN: config.ASSISTANCE_PLAN_ATTACHMENT_DIR,
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attachment_type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Unicode(150))
    dirname = db.Column(db.Unicode(200), nullable=False)
    filename = db.Column(db.Unicode(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user_.id'), nullable=True)
    teledoctor_doctor_id = db.Column(db.Integer, db.ForeignKey('user_.id'), nullable=True)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=STATUS_ACTIVE)
    card_wallet_id = db.Column(db.Integer, db.ForeignKey('card_wallet.id'), nullable=True)

    def __init__(self, *args, **kwargs):
        doctor = db.relationship(m.User, foreign_keys="[Attachment.teledoctor_doctor_id]")
        user = db.relationship(m.User, foreign_keys="[Attachment.user_id]")
        wallet = db.relationship(m.CardWallet, foreign_keys="[Attachment.card_wallet_id]")

    @classmethod
    def all_types(self):
        return [
            self.TYPE_ASSISTANCE_SALE,
            self.TYPE_INSURANCE_SALE,
            self.TYPE_INSURANCE_TICKET,
            self.TYPE_INSURANCE_PRODUCT,
            self.TYPE_MEDICAL_PROVIDER,
            self.TYPE_ASSISTANCE_PROVIDER,
            self.TYPE_ASSISTANCE_MAIL,
            self.TYPE_INSURANCE_ATTACHMENT,
            self.TYPE_MEDICAL_TICKET,
            self.TYPE_MEDICAL_PHARMACY_PRODUCT,
            self.TYPE_REPORT_ATTACHMENT,
            self.TYPE_CKEDITOR_IMAGE,
            self.TYPE_CAR,
            self.TYPE_TELEDOCTOR_SALE,
            self.TYPE_CRM_MAIL,
            self.TYPE_TELEDOCTOR_TICKET,
            self.TYPE_MEDICAL_PHARMACY_LOCATION_PRODUCT,
            self.TYPE_MEDICAL_PROVIDER_SERVICE_IMPORT,
            self.TYPE_MEDICAL_PROVIDER_LABORATORY_IMPORT,
            self.TYPE_MEDICAL_CONSULTATION_TICKET,
            self.TYPE_ASSISTANCE_MAIL_FILE,
            self.TYPE_SITE_LOGO,
            self.TYPE_SITE_FAVICON,
            self.TYPE_SITE_BACKGROUND,
            self.TYPE_SITE_HEADER,
            self.TYPE_SITE_FOOTER,
            self.TYPE_FRONTING_LOGO,
            self.TYPE_MEDICAL_PROVIDER_CHILDREN,
            self.TYPE_MEDICAL_CLAIM_TICKET,
            self.TYPE_INSURANCE_CASE_CLAIM,
            self.TYPE_ASSISTANCE_REPROCESS,
            self.TYPE_MEDICAL_CLAIM_TICKET,
            self.TYPE_MEDICAL_LOCATION_PROVIDERS,
            self.TYPE_ASSISTANCE_PAYMENT_BATCH,
            self.TYPE_ASSISTANCE_CREDIX_PROSPECTS,
            self.TYPE_ASSISTANCE_PLAN_MAIL,
            self.TYPE_ASSISTANCE_PLAN_MAIL_FILE,
            self.TYPE_ASSISTANCE_PLAN_APP_FILE,
            self.TYPE_MEDICAL_AUTHORIZATION_FILE,
            self.TYPE_MEDICAL_PAYMENT_BATCH,
            self.TYPE_ASSISTANCE_PROVIDER_BILL,
            self.TYPE_FINDING,
            self.Retroa_callback,
            self.Retroalimentación,
            self.Callback,
            self.monestación_proceso_disciplinario,
            self.Foto,
            self.Correos,
            self.Finiquitos,
            self.Solicitud,
            self.Apelacion,
            self.Analisis_del_hallazgo_por_oficial_riesgo,
            self.TYPE_WALLET_ASSET,
            self.TYPE_WALLET_ASSET_ICON,
            self.TYPE_WALLET_ASSET_ICON2X,
            self.TYPE_WALLET_ASSET_LOGO,
            self.TYPE_WALLET_ASSET_LOGO2X,
            self.TYPE_WALLET_ASSET_STRIP,
            self.TYPE_WALLET_ASSET_STRIP2X,
            self.TYPE_WALLET_ASSET_STRIP3X,
            self.TYPE_ASSISTANCE_PRODUCT,
            self.TYPE_ASSISTANCE_PLAN
    ]
