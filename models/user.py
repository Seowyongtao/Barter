from models.base_model import BaseModel
import peewee as pw
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=True)
    picture = pw.CharField(default='profile-placeholder.jpg')


    @hybrid_property
    def profile_image_url(self):
        return 'https://s3-ap-southeast-1.amazonaws.com/next-clone-instagram-hiro/' + self.picture

# class Following(BaseModel):
#     fan = pw.ForeignKeyField(User)
#     idol = pw.ForeignKeyField(User)