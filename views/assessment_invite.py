from flask import Blueprint, request, jsonify
from flask_mail import Message
from datetime import datetime
from models import db, AssessmentInvite, Student, AssessmentSubmission
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

from flask_mail import Message

@assessment_invite_bp.route("/assessment-invites", methods=["POST"])
@jwt_required()
def create_assessment_invites():
    data = request.get_json()

    # Validate required fields
    required_fields = ["assessment_id", "student_ids", "tm_id", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if not isinstance(data["student_ids"], list):
        return jsonify({"error": "student_ids must be a list of student IDs"}), 400

    assessment_id = data["assessment_id"]
    tm_id = data["tm_id"]
    status = data["status"]
    student_ids = data["student_ids"]

    invites_created = []
    invalid_students = []
    emails_sent = []
    new_invites = []
    skipped_students = []

    for student_id in student_ids:
        # Check if student exists
        student = Student.query.get(student_id)
        if not student:
            invalid_students.append(student_id)
            continue  # Skip invalid student IDs

        # Check if the student has already submitted this assessment
        submission_exists = AssessmentSubmission.query.filter_by(
            assessment_id=assessment_id, student_id=student_id
        ).first()

        if submission_exists:
            skipped_students.append(student.email)  # Track students who already submitted
            continue  # Skip sending invite & email

        # Create a new assessment invite
        new_invite = AssessmentInvite(
            assessment_id=assessment_id,
            student_id=student_id,
            tm_id=tm_id,
            status=status,  
            created_at=datetime.utcnow(),
            completed_at=None  
        )
        new_invites.append(new_invite)
        invites_created.append(student.email)

    # Batch insert for efficiency
    if new_invites:
        db.session.bulk_save_objects(new_invites)
        db.session.commit()

    # Send email to each invited student (only those who have not submitted before)
    for student_email in invites_created:
        student = Student.query.filter_by(email=student_email).first()
        if student:
            try:
                msg = Message('Assessment Invitation', recipients=[student.email])
                msg.body = f"""
                Hello {student.username},

                You have been invited to participate in an assessment.

                - Assessment ID: {assessment_id}
                - Status: Pending
                - Invited By: TM ID {tm_id}

                Please check your dashboard for more details.

                Regards,  
                Admin Team
                """
                mail.send(msg)
                emails_sent.append(student.email)
            except Exception as e:
                return jsonify({'message': 'Invite created, but email sending failed', 'error': str(e)}), 500

    return jsonify({
        'message': 'Assessment invites processed successfully',
        'invited_students': invites_created,
        'emails_sent': emails_sent,
        'invalid_students': invalid_students,
        'skipped_students': skipped_students  # Students who already submitted the assessment
    }), 201

    return jsonify({
        'message': 'Assessment invites sent successfully',
        'invited_students': invites_created,
        'emails_sent': emails_sent,
        'invalid_students': invalid_students
    }), 201


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
