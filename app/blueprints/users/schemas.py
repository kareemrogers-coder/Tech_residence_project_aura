from app.models import Users
from app.extensions import ma

class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
login_schema = UsersSchema(exclude=['name', 'phone', 'dob'])