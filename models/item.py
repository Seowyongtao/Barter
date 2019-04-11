import peewee as pw
from models.base_model import BaseModel
from sqlalchemy.ext.hybrid import hybrid_property
from models.user import User


class Item(BaseModel):
    file_name = pw.CharField(null=True)
    tag_parent = pw.CharField(null=True)
    tag_children = pw.CharField(null=True)
    description = pw.CharField(null=True,max_length=255)
    user = pw.ForeignKeyField(User, backref="user")

# we user to retrieve data from Amazon s3
    @hybrid_property
    def item_image_url(self):
        return 'https://s3-ap-southeast-1.amazonaws.com/next-clone-instagram-hiro/' + self.file_name

