from flask import Blueprint, request, jsonify
from flask_mail import Message
from datetime import datetime
from models import db, AssessmentInvite, Student
from flask_jwt_extended import jwt_required
from flask_mail import Mail

assessment_invite_bp = Blueprint('assessment_invite_bp', __name__)
mail = Mail()  # Ensure this is initialized in your Flask app

# Fetch all assessment invites
@assessment_invite_bp.route('/assessment-invites', methods=['GET'])
@jwt_required()
def get_assessment_invites():
    invites = AssessmentInvite.query.all()
    result = [
        {
            'id': invite.id,
            'assessment_id': invite.assessment_id,
            'student_id': invite.student_id,
            'tm_id': invite.tm_id,
            'status': invite.status,
            'created_at': invite.created_at.isoformat(),
            'completed_at': invite.completed_at.isoformat() if invite.completed_at else None
        } for invite in invites
    ]
    return jsonify(result), 200

# Create an assessment invite
@assessment_invite_bp.route("/assessment-invites", methods=["POST"])
@jwt_required()
def create_assessment_invite():
    data = request.get_json()

    # Validate required fields
    required_fields = ["assessment_id", "student_ids", "tm_id", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Create new assessment invites for each student
    for student_id in data["student_ids"]:
        new_invite = AssessmentInvite(
            assessment_id=data["assessment_id"],
            student_id=student_id,
            tm_id=data["tm_id"],
            status=data["status"],  # Example: 'pending', 'accepted', 'declined'
            created_at=datetime.utcnow(),
            completed_at=None  # Set when assessment is completed
        )

        db.session.add(new_invite)

    db.session.commit()

    # Fetch student details and send emails
    for student_id in data["student_ids"]:
        student = Student.query.get(student_id)
        if not student:
            return jsonify({"error": f"Student not found: {student_id}"}), 404

        try:
            msg = Message('Assessment Invitation', recipients=[student.email])
            msg.body = f"""
            Hello {student.username},

            You have been invited to participate in an assessment.

            - Assessment ID: {data['assessment_id']}
            - Status: Pending
            - Invited By: TM ID {data['tm_id']}

            Please check your dashboard for more details.

            Regards,  
            Admin Team
            """
            mail.send(msg)
        except Exception as e:
            return jsonify({'message': 'Invite created, but email sending failed', 'error': str(e)}), 500

    return jsonify({'message': 'Assessment invites sent successfully'}), 201

    # Send email to invited student
    try:
        msg = Message('Assessment Invitation', recipients=[student.email])
        msg.body = f"""
        Hello {student.username},

        You have been invited to participate in an assessment.

        - Assessment ID: {data['assessment_id']}
        - Status: Pending
        - Invited By: TM ID {data['tm_id']}

        Please check your dashboard for more details.

        Regards,  
        Admin Team
        """
        mail.send(msg)
    except Exception as e:
        return jsonify({'message': 'Invite created, but email sending failed', 'error': str(e)}), 500

    return jsonify({'message': 'Assessment invite sent successfully', 'invite_id': new_invite.id}), 201

# Update an existing assessment invite
@assessment_invite_bp.route('/assessment-invites/<int:id>', methods=['PATCH'])
@jwt_required()
def update_assessment_invite(id):
    data = request.get_json()
    invite = AssessmentInvite.query.get_or_404(id)

    invite.assessment_id = data.get('assessment_id', invite.assessment_id)
    invite.student_id = data.get('student_id', invite.student_id)
    invite.tm_id = data.get('tm_id', invite.tm_id)
    invite.status = data.get('status', invite.status)
    invite.completed_at = datetime.fromisoformat(data['completed_at']) if 'completed_at' in data else invite.completed_at

    db.session.commit()
    return jsonify({'message': 'Assessment invite updated successfully'}), 200

# Delete an existing assessment invite
@assessment_invite_bp.route('/assessment-invites/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_assessment_invite(id):
    invite = AssessmentInvite.query.get_or_404(id)
    db.session.delete(invite)
    db.session.commit()
    return jsonify({'message': 'Assessment invite deleted successfully'}), 200
