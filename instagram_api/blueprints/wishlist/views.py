from flask import Blueprint
from flask import Blueprint, request,jsonify
import os
from models.item import Item
from models.user import User
from models.wishlist import Wishlist



from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

wishlist_api_blueprint = Blueprint('Wishlist_api',
                             __name__,
                             template_folder='templates')



@wishlist_api_blueprint.route('/new', methods=['POST'])
@jwt_required
def create():
    id = get_jwt_identity()
    user = User.get(User.id == id)

    item_id = request.json.get('item_id', None)

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if not id:
        return jsonify({"msg": "Missing user_id parameter"}), 400
    if not item_id:
        return jsonify({"msg": "Missing item_id parameter"}), 400
  
    us= Wishlist(user_id=user.id, item_id=item_id )

    if  item_id and user:
        us.save()
        return jsonify({"msg":"you adding is successful"}),200
   
    else:
        return jsonify({"msg":"same username already exist"}),400
        
  

                           