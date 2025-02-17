from flask import jsonify, request, Blueprint
from flask_mail import Message
from models import db, Users
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


user_bp = Blueprint("user_bp", __name__)




#=================================================getting all users============================
@user_bp.route("/users")
def fetch_users():
    users = Users.query.all()

    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'username': user.username,
        })

    return jsonify(user_list)