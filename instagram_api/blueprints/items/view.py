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
    tag_parent = request.json.get('tag_parent', None)
    tag_children = request.json.get('tag_children', None)
    description = request.json.get('description', None)
    id = get_jwt_identity()
    

    if not file_name:
        return jsonify({"msg": "Missing file_name parameter"}), 400
    if not tag_parent:
        return jsonify({"msg": "Missing tag_parent parameter"}), 400
    if not tag_children:
        return jsonify({"msg": "Missing tag_children parameter"}), 400
    if not description:
        return jsonify({"msg": "Missing description parameter"}), 400

    username_check = User.get_or_none(User.id == id)
    
    item = Item(file_name=file_name,tag_parent=tag_parent,tag_children=tag_children,description=description, user_id=username_check.id)
    item.save()
    return jsonify({
    "message": "Successfully make a new item.",
    "status": "success",
    "user": {
        "id": username_check.id,
        "tag_parent": tag_parent,
        "tag_children": tag_children,
        "description": description,
        "file_name": file_name
    }
    }), 200
  


# edit item information
@item_api_blueprint.route('/edit/<id>', methods=['POST'])
@jwt_required
def edit(id):
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    file_name= request.json.get('file_name', None)
    tag_parent = request.json.get('tag_parent', None)
    tag_children = request.json.get('tag_children', None)
    description = request.json.get('description', None)
<<<<<<< HEAD
    id = get_jwt_identity()
=======
    # username = get_jwt_identity()
>>>>>>> f0610b73ef70f347ecda5b90535c03d7c28dc87e
    

    if not file_name:
        return jsonify({"msg": "Missing file_name parameter"}), 400
    if not tag_parent:
        return jsonify({"msg": "Missing tag_parent parameter"}), 400
    if not tag_children:
        return jsonify({"msg": "Missing tag_children parameter"}), 400
    if not description:
        return jsonify({"msg": "Missing description parameter"}), 400

<<<<<<< HEAD
    username_check = User.get_or_none(User.id == id)
=======
    item = Item.get_or_none(Item.id == id)
>>>>>>> f0610b73ef70f347ecda5b90535c03d7c28dc87e
    
    item.file_name = file_name
    item.tag_parent = tag_parent
    item.tag_children = tag_children
    item.description = description
    item.save()
    return jsonify({
    "message": "Successfully update a new item.",
    "status": "success",
    "user": {
        "id": item.id,
        "tag_children": tag_children,
        "tag_parent": tag_parent,
        "file_name": file_name
    }
    }), 200


# show item information
@item_api_blueprint.route('/show/items/me', methods=['GET'])
@jwt_required
def showw_me():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)
    user_id = user.id
    items = Item.select().where(Item.user_id == user_id)

    return jsonify({
        "status": "success",
        "user": [{
            "file_name": item.file_name,
            "tag_parent": item.tag_parent,
            "tag_children": item.tag_children,
            "description": item.description
        } for item in items]
        }), 200
  
  

# show items information with filters
@item_api_blueprint.route('/show/items/<place>/<tag_parent>', methods=['GET'])
@jwt_required
def show_items(place,tag_parent):
    
    if request.args:
        tag_children = request.args['tag_children']
        items = (Item.select(Item,User).join(User).where(User.location == place and Item.tag_children == tag_children))

    else:
        items = (Item.select(Item,User).join(User).where(User.location == place and Item.tag_parent == tag_parent))
    
    return jsonify({
        "status": "success",
        "user": [{  
            "file_name": item.file_name,
            "tag_parent": item.tag_parent,
            "tag_children": item.tag_children,
            "description": item.description,
            "owner_name": item.user.username,
            "owner_location": item.user.location
        } for item in items]
        }), 200
