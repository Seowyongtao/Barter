from flask import Blueprint, request,jsonify
import os
from models.user import User
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity
)
from werkzeug.security import check_password_hash
from app import csrf
import datetime

login_api_blueprint = Blueprint('login_api',
                             __name__,
                             template_folder='templates')

    
@login_api_blueprint.route('/login', methods=['POST'])
@csrf.exempt
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    time = request.json.get('time', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.get_or_none(User.username == username)
    if user and check_password_hash(user.password, password):
        user.last_login = time
        user.save()
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=username)
        return jsonify({
            "access_token": access_token,
            "message": "Successfully signed in.",
            "status": "success",
            "user": {
                "id": user.id,
                "profile_picture": user.profile_image_url,
                "username": user.username
            }
        }), 200
    else:
        return jsonify({"msg": "Bad login"}), 404


