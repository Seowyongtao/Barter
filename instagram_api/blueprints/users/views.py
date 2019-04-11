from flask import Blueprint
from flask import Blueprint, request,jsonify
from flask import render_template,redirect,request,url_for,session,flash,escape
import os

import re
from models.user import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity, 
    jwt_required
)


users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    return "username: hiro"


@users_api_blueprint.route('/new', methods=['POST'])
def create():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    email = request.json.get('email',None)
    

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400

    # actual sign up users 
    user_password = password
    hashed_password = generate_password_hash(user_password)

    # front_end side will do the validation
    # pattern_password = '\w{6,}'
    # result = re.search(pattern_password, user_password)
    # pattern_email = '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]'
    # result_email = re.search(pattern_email,email)

    username_check = User.get_or_none(User.username == username)
    email_check = User.get_or_none(User.email == email)
    
    # if (result and result_email):
    u = User(username=username,email=email,password=hashed_password)

    if not username_check and not email_check:
        u.save()
        user = User.get(User.username == username)
        access_token = create_access_token(identity=username)
        return jsonify({
        "access_token": access_token,
        "message": "Successfully created a user and signed in.",
        "status": "success",
        "user": {
            "id": user.id,
            "profile_picture": user.profile_image_url,
            "username": user.username
        }
    }), 200
    else:
        return jsonify({"msg": "username or email already used"}), 400
  



@users_api_blueprint.route('/new/show_profilepag', methods=['GET'])
@jwt_required
def show_profilepag():
    username = get_jwt_identity()
    user = User.get_or_none(User.username == username)

    if user:
        return jsonify({
            "status":"success",
            "user":{
                "username": user.username,
                "firstname":user.firstname,
                "lastname": user.lastname,
                "occupation": user.occupation,
                "location": user.location,
                "sex": user.sex,
                "going_to": user.going_to,
                "date" : user.date,
                "birthday": user.birthday,
                "brif": user.brif
            }
        }), 200
