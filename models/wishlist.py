from models.base_model import BaseModel
import peewee as pw
from sqlalchemy.ext.hybrid import hybrid_property
from models.user import User
from models.item import Item


class Wishlist(BaseModel):
    user = pw.ForeignKeyField(User)
    item = pw.ForeignKeyField(Item) 


    @hybrid_property
    def profile_image_url(self):
        return 'https://s3-ap-southeast-1.amazonaws.com/next-clone-instagram-hiro/' + self.picture
