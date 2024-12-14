from app.models import LeaderboardLike
from app.extensions import ma

class LeaderboardLikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LeaderboardLike


leaderboardlike_schema = LeaderboardLikeSchema()
leaderboardlikes_schema = LeaderboardLikeSchema(many=True)