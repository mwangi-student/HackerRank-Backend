from flask import jsonify, request, Blueprint
from models import db, TM, Student, TokenBlocklist
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, timezone

auth_bp = Blueprint("auth_bp", __name__)

# ============================== LOGIN (for both Student & TM) ==============================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user is a Student
    user = Student.query.filter_by(email=email).first()
    role = "student" if user else None

    # If not a student, check if user is a TM
    if not user:
        user = TM.query.filter_by(email=email).first()
        role = "tm" if user else None

    # If no user found, return error
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    access_token = create_access_token(
        identity={"id": user.id, "role": role}, 
        expires_delta=timedelta(hours=24)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": role  # Now role is determined automatically
        }
    }), 200


# ============================== GET CURRENT USER ==============================
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    user_id = identity["id"]
    role = identity["role"]

    if role == "student":
        user = Student.query.get(user_id)
    elif role == "tm":
        user = TM.query.get(user_id)
    else:
        return jsonify({"error": "Invalid user role"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": role
    }), 200



# ============================== LOGOUT ==============================
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get JWT's unique identifier
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now(timezone.utc)))
    db.session.commit()
    return jsonify({"message": "Successfully logged out"}), 200
