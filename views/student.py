from flask import jsonify, request, Blueprint
from flask_mail import Message
from models import db, Student
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

student_bp = Blueprint("student_bp", __name__)

#=================================================creating a new student============================
@student_bp.route("/students", methods=["POST"])
@cross_origin(origin="http://localhost:5173", supports_credentials=True)
def create_student():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    cohort = data.get("cohort")
    tm_id = data.get("tm_id") 

    hashed_password = generate_password_hash(password)

    new_student = Student(
        username=username,
        email=email,
        password=hashed_password,
        cohort=cohort,
        tm_id=tm_id
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": {
            'id': new_student.id,
            'email': new_student.email,
            'username': new_student.username,
            'cohort': new_student.cohort,
            'created_at': new_student.created_at
        }
    }), 201

#=================================================getting all users============================
@student_bp.route("/students", methods=["GET"])
def fetch_students():
    students = Student.query.all()

    student_list = []
    for student in students:
        student_list.append({
            'id': student.id,
            'email': student.email,
            'username': student.username,
            'cohort': student.cohort,
            'created_at': student.created_at,
            'tm_id':student.tm_id
        })

    return jsonify(student_list)


#=================================================getting a single student============================
@student_bp.route("/students/<int:id>", methods=["GET"])
def fetch_student(id):
    student = Student.query.get(id)
    if student:
        return jsonify({
            'id': student.id,
            'email': student.email,
            'username': student.username,
            'cohort': student.cohort,
            'created_at': student.created_at,
            'tm_id':student.tm_id
        })
    return jsonify({"message": "Student not found!"}), 404


#=================================================updating an existing student============================
@student_bp.route("/students/<int:id>", methods=["PATCH"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found!"}), 404

    data = request.get_json()
    student.username = data.get("username", student.username)
    student.email = data.get("email", student.email)
    student.password = generate_password_hash(data.get("password", student.password))
    student.cohort = data.get("cohort", student.cohort)
    student.tm_id = data.get("tm_id", student.tm_id)
 

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": {
            'id': student.id,
            'email': student.email,
            'username': student.username,
            'cohort': student.cohort,
            'created_at': student.created_at,
            'tm_id':student.tm_id
        }
    })

