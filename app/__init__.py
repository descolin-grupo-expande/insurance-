from flask import Flask
from app.config.common import Config
from app.extensions import db
from app.routes.users import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    return app