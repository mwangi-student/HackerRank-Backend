from flask import Blueprint, request, jsonify
from flask_mail import Message
from models import db, AssessmentInvite, Student
from flask_jwt_extended import jwt_required, get_jwt_identity


assessment_invite_bp = Blueprint('assessment_invite_bp', __name__)

# Fetch all assessment invites
@assessment_invite_bp.route('/assessment-invite', methods=['GET'])
@jwt_required()
def get_assessment_invites():
    invites = AssessmentInvite.query.all()
    result = [
        {
            'id': invite.id,
            'assessment_id': invite.assessment_id,
            'student_id': invite.student_id,
            'invited_by': invite.invited_by,
            'status': invite.status
        } for invite in invites
    ]
    return jsonify(result)

# Fetch a single assessment invite by ID
@assessment_invite_bp.route('/assessment-invite/<int:id>', methods=['GET'])
@jwt_required()
def get_assessment_invite(id):
    invite = AssessmentInvite.query.get_or_404(id)
    result = {
        'id': invite.id,
        'assessment_id': invite.assessment_id,
        'student_id': invite.student_id,
        'invited_by': invite.invited_by,
        'status': invite.status
    }
    return jsonify(result)

# Create a new assessment invite
@assessment_invite_bp.route('/assessment-invite', methods=['POST'])
@jwt_required()
def create_assessment_invite():

    from flask_mail import mail

    data = request.get_json()
    assessment_id = data.get('assessment_id')
    invited_by = get_jwt_identity()  # Get TM ID of the logged-in user

    # Fetch all students
    students = Student.query.all()

    if not students:
        return jsonify({'error': 'No students found'}), 404

    # List to track invited students
    invited_students = []

    for student in students:
        new_invite = AssessmentInvite(
            assessment_id=assessment_id,
            student_id=student.id,
            invited_by=invited_by,
            status="Pending"  # Default status
        )
        db.session.add(new_invite)
        invited_students.append(student)

    db.session.commit()

    # Send emails to all invited students
    try:
        for student in invited_students:
            msg = Message('Assessment Invitation', recipients=[student.email])
            msg.body = f"""
            Hello {student.username},

            You have been invited to participate in an assessment.

            - Assessment ID: {assessment_id}
            - Status: Pending
            - Invited By: TM ID {invited_by}

            Please check your dashboard for more details.

            Regards,  
            Admin Team
            """
            mail.send(msg)

    except Exception as e:
        return jsonify({'message': 'Invites created, but email sending failed', 'error': str(e)}), 500

    return jsonify({'message': 'Assessment invites sent successfully'}), 201

# Update an existing assessment invite
@assessment_invite_bp.route('/assessment-invite/<int:id>', methods=['PATCH'])
@jwt_required()
def update_assessment_invite(id):
    data = request.get_json()
    invite = AssessmentInvite.query.get_or_404(id)

    invite.assessment_id = data.get('assessment_id', invite.assessment_id)
    invite.student_id = data.get('student_id', invite.student_id)
    invite.invited_by = data.get('invited_by', invite.invited_by)
    invite.status = data.get('status', invite.status)

    db.session.commit() 
    return jsonify({'message': 'Assessment invite updated successfully'})

# Delete an existing assessment invite
@assessment_invite_bp.route('/assessment-invite/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_assessment_invite(id):
    invite = AssessmentInvite.query.get_or_404(id)
    db.session.delete(invite) 
    db.session.commit()
    return jsonify({'message': 'Assessment invite deleted successfully'})
