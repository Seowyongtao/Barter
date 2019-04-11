from models.base_model import BaseModel
import peewee as pw
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=True)
    # picture = pw.CharField(default='profile-placeholder.jpg')

    firstname = pw.CharField( null=True)
    lastname = pw.CharField( null=True)   
    occupation = pw.CharField( null=True)      
    location = pw.CharField( null=True)      
    sex = pw.CharField( null=True)              
    going_to = pw.CharField( null=True)
    date = pw.CharField( null=True)      
    birthday = pw.CharField( null=True)      
    brif = pw.CharField( null=True)      

    @hybrid_property
    def profile_image_url(self):
        return 'https://s3-ap-southeast-1.amazonaws.com/next-clone-instagram-hiro/' + self.picture

    

