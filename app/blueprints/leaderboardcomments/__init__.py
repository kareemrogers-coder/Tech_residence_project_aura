from flask import Blueprint

leaderboardcomments_bp = Blueprint('leaderboardcomments_bp', __name__)

from . import routes