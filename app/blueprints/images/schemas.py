from app.models import Images
from app.extensions import ma

class ImagesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Images

image_schema = ImagesSchema()
image_schema = ImagesSchema(many=True)
