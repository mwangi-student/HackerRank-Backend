from flask import jsonify, request, Blueprint, current_app
from models import db, Student, TM
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from flask_mail import Message



student_bp = Blueprint("student_bp", __name__)

#=================================================creating a new student============================
@student_bp.route("/students", methods=["POST"])
@cross_origin(origin="http://localhost:5173", supports_credentials=True)
def create_student():
    mail = current_app.extensions.get("mail")

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

    
    # Get TM details
    tm = TM.query.get(tm_id)

    # Sending Emails
    try:
        # Email to Student
        student_msg = Message('Welcome to the System', recipients=[new_student.email])
        student_msg.body = f"""
        Hello {new_student.username},

        Your student account has been successfully created.

        Here are your login details:
        Email: {new_student.email}
        Password: {password}

        Please keep your credentials safe.

        Regards,
        Admin Team
        """
        mail.send(student_msg)

        # Email to TM (if found)
        if tm:
            tm_msg = Message('New Student Registered', recipients=[tm.email])
            tm_msg.body = f"""
            Hello {tm.username},

            A new student has been registered under your supervision.

            Student Details:
            Username: {new_student.username}
            Email: {new_student.email}
            Cohort: {new_student.cohort}

            Regards,
            Admin Team
            """
            mail.send(tm_msg)

    except Exception as e:
        return jsonify({'message': 'Student created, but email sending failed', 'error': str(e)}), 500

    return jsonify({
        "message": "Student created successfully, emails sent",
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
@jwt_required()
def fetch_students():
    try:
        students = Student.query.all()
        student_list = [
            {
                'id': student.id,
                'email': student.email,
                'username': student.username,
                'cohort': student.cohort,
                'created_at': student.created_at,
                'tm_id': student.tm_id
            }
            for student in students
        ]
        return jsonify(student_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#=================================================getting a single student============================
@student_bp.route("/students/<int:id>", methods=["GET"])
@jwt_required()
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
@jwt_required()
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

