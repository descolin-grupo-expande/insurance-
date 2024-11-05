from flask import Flask
# from app.config.common import Config
from app.config.appconfig import AppConfig
from app.extensions import db
from app.routes.users import user_bp
from app.routes.assistances import assistances_bp
from app.routes.cars import cars_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    config = AppConfig()
    app.config.from_object(config)
    
    db.init_app(app)
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(assistances_bp, url_prefix='/api/assistance')
    app.register_blueprint(cars_bp, url_prefix='/api/cars')
    
    return app