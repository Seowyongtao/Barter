from flask import Blueprint
from flask import Blueprint, request,jsonify
import os
from models.item import Item
from models.user import User

from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

item_api_blueprint = Blueprint('item_api',
                             __name__,
                             template_folder='templates')


@item_api_blueprint.route('/new', methods=['POST'])
@jwt_required
def create():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    file_name= request.json.get('username', None)
    tag = request.json.get('password', None)
    username = get_jwt_identity()
    

    if not file_name:
        return jsonify({"msg": "Missing file_name parameter"}), 400
    if not tag:
        return jsonify({"msg": "Missing tag parameter"}), 400

    username_check = User.get_or_none(User.username == username)
    
    
    if not username_check:
        
        item = Item(file_name=file_name,tag=tag,user_id=username_check.id)
        item.save()
        return jsonify({
        "message": "Successfully make a new item.",
        "status": "success",
        "user": {
            "id": username_check.id,
            "tag": tag,
            "file_name": file_name
        }
    }), 200
    # else:
    #     return jsonify({"msg": "JWT is invalid"}), 400
  