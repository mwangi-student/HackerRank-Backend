from flask import jsonify, request, Blueprint, current_app
from models import db, TM, Student, TokenBlocklist
from flask_mail import Message

from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt, decode_token
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

# google signin
@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    data = request.get_json()
    id_token_str = data.get("idToken")

    try:
        # Verify Google token
        google_info = id_token.verify_oauth2_token(id_token_str, requests.Request())
        email = google_info["email"]
        
        # Find or create user in database
        user = Student.query.filter_by(email=email).first() or TM.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Generate JWT
        role = "student" if isinstance(user, Student) else "tm"
        access_token = create_access_token(identity={"id": user.id, "role": role})

        return jsonify({
            "message": "Google login successful",
            "access_token": access_token,
            "user": {"id": user.id, "username": user.username, "email": user.email, "role": role}
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 401


# ============================== GET CURRENT USER ==============================
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def get_current_user():
    identity = get_jwt_identity()
    print("Identity:", identity)  # Debugging

    if not identity or "id" not in identity or "role" not in identity:
        return jsonify({"error": "Invalid token payload"}), 422

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

# =================================password reset email
@auth_bp.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    mail = current_app.extensions.get("mail")

    data = request.get_json()
    email = data.get("email")

    # Check if the user exists in tm or student table
    user = TM.query.filter_by(email=email).first() or Student.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Generate a password reset token (valid for 30 minutes)
    expires = timedelta(minutes=30)
    reset_token = create_access_token(identity={"id": user.id, "role": user.__class__.__name__}, expires_delta=expires)

    # Create the reset email
    reset_link = f"http://localhost:5173/reset-password/{reset_token}"  # Change to your frontend URL
    msg = Message("Password Reset Request", recipients=[email])
    msg.body = f"Click the link below to reset your password:\n\n{reset_link}\n\nThis link expires in 30 minutes."

    # Send the email
    try:
        mail.send(msg)
        return jsonify({"message": "Password reset email sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
#========================================================= password reseting function
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"message": "Invalid request"}), 400

    try:
        # Decode the token and get user identity
        decoded_token = decode_token(token)
        user_id = decoded_token["sub"]["id"]
        user_role = decoded_token["sub"]["role"]

        # Find user in the database
        user = TM.query.get(user_id) if user_role == "TM" else Student.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Hash the new password (Ensure you're using Flask-Bcrypt for password hashing)
        from werkzeug.security import generate_password_hash
        user.password = generate_password_hash(new_password)

        # Save the updated password in the database
        db.session.commit()

        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# ============================== LOGOUT ==============================
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get JWT's unique identifier
    db.session.add(TokenBlocklist(jti=jti, created_at=datetime.now(timezone.utc)))
    db.session.commit()
    return jsonify({"message": "Successfully logged out"}), 200
