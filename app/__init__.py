from flask import Flask, jsonify
from app.models import db
from app.extensions import ma, limiter
from app.blueprints.users import users_bp
from app.blueprints.images import images_bp
from app.blueprints.leaderboard import leaderboard_bp
from app.blueprints.leaderboardcomments import leaderboardcomments_bp
from app.blueprints.leaderboardlike import leaderboardlike_bp
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
    app.register_blueprint(leaderboard_bp, url_perfix = "/leaderboard")
    app.register_blueprint(leaderboardcomments_bp, url_perfix = "/leaderboardcomments")
    app.register_blueprint(leaderboardlike_bp, url_perfix = "/leaderboardlike")

    @app.route('/')
    def home():
        return jsonify({"Message": "Welcome to Aura API"})

    return app

