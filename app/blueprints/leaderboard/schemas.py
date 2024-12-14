from app.models import Leaderboard
from app.extensions import ma

class LeaderboardSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Leaderboard

leaderboard_schema = LeaderboardSchema()
leaderboards_schema = LeaderboardSchema(many = True)