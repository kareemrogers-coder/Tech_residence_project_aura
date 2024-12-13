from flask import Flask
from app.models import db
from app.extensions import ma, limiter
from app.blueprints.users import users_bp
from app.blueprints.images import images_bp
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def create_app(config_name):
    app= Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    #extension
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)

    ## register blueprint
    app.register_blueprint(users_bp, url_prefix ="/users")
    app.register_blueprint(images_bp, url_prefix ="/images")

    return app