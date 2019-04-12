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
    return "USERS API"


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
        access_token = create_access_token(identity=user.id)
        return jsonify({
        "access_token": access_token,
        "message": "Successfully created a user and signed in.",
        "status": "success",
        "user": {
            "id": user.id,
            # "profile_picture": user.profile_image_url,
            "username": user.username
        }
    }), 200
    else:
        return jsonify({"msg": "username or email already used"}), 400
  



@users_api_blueprint.route('/new/show_profilepag', methods=['GET'])
@jwt_required
def show_profilepag():
    id = get_jwt_identity()
    user = User.get_or_none(User.id == id)

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



@users_api_blueprint.route('/new/edit_profilepag', methods=['POST'])
@jwt_required
def edit_profilepag():
    id = get_jwt_identity()
    user = User.get(User.id == id)

    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    firstname = request.json.get('firstname', None)
    lastname = request.json.get('lastname',None)
    location = request.json.get('location',None)
    going_to = request.json.get('going_to',None)
    brif = request.json.get('brif',None)
    sex = request.json.get('sex',None)
    occupation = request.json.get('occupation',None)
    date = request.json.get('date',None)
    birthday = request.json.get('birthday',None)
    

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not firstname:
        return jsonify({"msg": "Missing firstname parameter"}), 400
    if not lastname:
        return jsonify({"msg": "Missing lastname parameter"}), 400
    if not location:
        return jsonify({"msg": "Missing location parameter"}), 400
    if not going_to:
        return jsonify({"msg": "Missing going_to parameter"}), 400
    if not brif:
        return jsonify({"msg": "Missing brif parameter"}), 400
    if not occupation:
        return jsonify({"msg": "Missing occupation parameter"}), 400
    if not date:
        return jsonify({"msg": "Missing date parameter"}), 400
    if not birthday:
        return jsonify({"msg": "Missing birthday parameter"}), 400
    if not sex:
        return jsonify({"msg": "Missing sex parameter"}), 400    


    username_check = User.get_or_none((User.username == username) )

    if not username_check:
        us= (User.update({User.username:username,  User.firstname:firstname,  User.lastname:lastname, User.location:location, User.going_to:going_to, User.brif:brif, User.occupation:occupation, User.date:date, User.birthday:birthday, User.sex:sex} ).where(User.id==id))
        us.execute()
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
   
    elif user.username == username:
        us= (User.update({User.firstname:firstname,  User.lastname:lastname, User.location:location, User.going_to:going_to, User.brif:brif, User.occupation:occupation, User.date:date, User.birthday:birthday, User.sex:sex} ).where(User.id==id))
        us.execute()
        return jsonify({
            "status":"success",
            "user":{
                
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
   
    else:
        return jsonify({"msg":"same username already exist"})
        

    # if(not user.username == username) {
    #     us= (User.update({User.username:username,  User.firstname:firstname,  User.lastname:lastname, User.location:location, User.going_to:going_to, User.brif:brif, User.occupation:occupation, User.date:date, User.birthday:birthday, User.sex:sex} ).where(User.id==id))
    # } else {
    #     us= (User.update({User.firstname:firstname,  User.lastname:lastname, User.location:location, User.going_to:going_to, User.brif:brif, User.occupation:occupation, User.date:date, User.birthday:birthday, User.sex:sex} ).where(User.id==id))
    # }
    

    # username_same= User.get_or_none((username == user.username))
    # firstname_check = User.get_or_none(User.firstname == firstname)
    # lastname_check = User.get_or_none(User.lastname == lastname)
    
    # us= (User.update({User.username:username,  User.firstname:firstname,  User.lastname:lastname, User.location:location, User.going_to:going_to, User.brif:brif, User.occupation:occupation, User.date:date, User.birthday:birthday, User.sex:sex} ).where(User.id==id))

    
      

        
