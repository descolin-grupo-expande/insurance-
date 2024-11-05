from flask import Flask
# from app.config.common import Config
from app.config.appconfig import AppConfig
from app.extensions import db
from app.routes.users import user_bp
from app.routes.assistances import assistances_bp
from app.routes.cars import cars_bp
from app.routes.auth import auth_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={
    r"*": {
        "origins": [
            r".*tec-seguros.*",
            r".*teledoctor.*",
            r"http://localhost.*",
            r"https://localhost.*",
            # Teledoctor
            r".*35.196.207.125.*",
            r".*tdasistencia.*",
            # Broker
            r".*35.196.248.242.*",
            # Policy Integrator
            r".*policy-integrator.*",
            r".*dev.s2plus.online.*",
            #Projections
            r".*financial-projections.*",
            r".*credix.asiasistencias.*",
            r".*unillantas.asiasistencias.*",
            #Other
            r".*sigep.gt-complementa.*",
            r".*customer-mailing.*",
            r"capacitor://localhost.*",
            r".*appspot.*",
            r".*grupoasys.*",
        ]
    })
    #CORS(app)
    #CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, methods=["GET", "POST", "OPTIONS"])
    config = AppConfig()
    app.config.from_object(config)
    
    db.init_app(app)
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(assistances_bp, url_prefix='/api/assistance')
    app.register_blueprint(cars_bp, url_prefix='/api/cars')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return app