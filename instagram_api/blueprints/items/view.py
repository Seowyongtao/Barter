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
def new():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    file_name= request.json.get('file_name', None)
    tag = request.json.get('tag', None)
    description = request.json.get('description', None)
    id = get_jwt_identity()
    

    if not file_name:
        return jsonify({"msg": "Missing file_name parameter"}), 400
    if not tag:
        return jsonify({"msg": "Missing tag parameter"}), 400
    if not description:
        return jsonify({"msg": "Missing description parameter"}), 400

    username_check = User.get_or_none(User.id == id)
    
    item = Item(file_name=file_name,tag=tag,description=description, user_id=username_check.id)
    item.save()
    return jsonify({
    "message": "Successfully make a new item.",
    "status": "success",
    "user": {
        "id": username_check.id,
        "tag": tag,
        "description": description,
        "file_name": file_name
    }
    }), 200
  


# edit item information
@item_api_blueprint.route('/edit', methods=['POST'])
@jwt_required
def edit():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    file_name= request.json.get('file_name', None)
    tag = request.json.get('tag', None)
    description = request.json.get('description', None)
    id = get_jwt_identity()
    

    if not file_name:
        return jsonify({"msg": "Missing file_name parameter"}), 400
    if not tag:
        return jsonify({"msg": "Missing tag parameter"}), 400
    if not description:
        return jsonify({"msg": "Missing description parameter"}), 400

    username_check = User.get_or_none(User.id == id)
    
    username_check.file_name = file_name
    username_check.tag = tag
    username_check.description = description
    username_check.save()
    return jsonify({
    "message": "Successfully update a new item.",
    "status": "success",
    "user": {
        "id": username_check.id,
        "tag": tag,
        "file_name": file_name
    }
    }), 200
  