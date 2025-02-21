from flask import Blueprint, request, jsonify
from models import db, AssessmentInvite

assessment_invite_bp = Blueprint('assessment_invite_bp', __name__)

# Fetch all assessment invites
@assessment_invite_bp.route('/assessment-invite', methods=['GET'])
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
def create_assessment_invite():
    data = request.get_json()
    new_invite = AssessmentInvite(
        assessment_id=data['assessment_id'],
        student_id=data['student_id'],
        invited_by=data['invited_by'],
        status=data['status']
    )
    db.session.add(new_invite) 
    db.session.commit()
    return jsonify({'message': 'Assessment invite created successfully'}), 201

# Update an existing assessment invite
@assessment_invite_bp.route('/assessment-invite/<int:id>', methods=['PATCH'])
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
def delete_assessment_invite(id):
    invite = AssessmentInvite.query.get_or_404(id)
    db.session.delete(invite) 
    db.session.commit()
    return jsonify({'message': 'Assessment invite deleted successfully'})
