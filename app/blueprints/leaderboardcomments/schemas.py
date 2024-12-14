from app.models import LeaderboardComment
from app.extensions import ma

class LeaderbaordCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LeaderboardComment

leaderboardcomment_schema = LeaderbaordCommentSchema()
leaderboardcomments_schema = LeaderbaordCommentSchema(many=True)
