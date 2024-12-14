from flask import Blueprint

leaderboard_bp = Blueprint('leaderboard_bp', __name__)

from . import routes