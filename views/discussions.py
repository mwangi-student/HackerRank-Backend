from flask import Blueprint, request, jsonify
from models import db, Discussion
from flask_jwt_extended import jwt_required, get_jwt_identity


# Blueprint setup
discussion_bp = Blueprint('discussion', __name__)

# ==========================================================Create Discussion
@discussion_bp.route('/discussion', methods=['POST'])
@jwt_required()
def create_discussion():
    data = request.get_json()
    # get the current user (TM )
    tm_id = get_jwt_identity()

    new_discussion = Discussion(
        assessment_id=data.get('assessment_id'),
        user_type=data.get('user_type'),
        student_id=data.get('student_id'),
        tm_id=tm_id,
        comment=data.get('comment')
    )
    db.session.add(new_discussion)
    db.session.commit()
    return jsonify({'message': 'Discussion created successfully'}), 201

# =================================================================Read All Discussions
@discussion_bp.route('/discussion', methods=['GET'])
@jwt_required()
def get_all_discussions():
    discussions = Discussion.query.all()
    result = []
    for discussion in discussions:
        result.append({
            'id': discussion.id,
            'assessment_id': discussion.assessment_id,
            'user_type': discussion.user_type,
            'student_id': discussion.student_id,
            'tm_id': discussion.tm_id,
            'comment': discussion.comment,
            'posted_at': discussion.posted_at
        })
    return jsonify(result), 200

# ========================================================================Read Single Discussion
@discussion_bp.route('/discussion/<int:discussion_id>', methods=['GET'])
@jwt_required()
def get_discussion(discussion_id):
    discussion = Discussion.query.get_or_404(discussion_id)
    return jsonify({
        'id': discussion.id,
        'assessment_id': discussion.assessment_id,
        'user_type': discussion.user_type,
        'student_id': discussion.student_id,
        'tm_id': discussion.tm_id,
        'comment': discussion.comment,
        'posted_at': discussion.posted_at
    }), 200

# ============================================================================Update Discussion
@discussion_bp.route('/discussion/<int:discussion_id>', methods=['PATCH'])
@jwt_required()
def update_discussion(discussion_id):
    discussion = Discussion.query.get_or_404(discussion_id)
    data = request.get_json()
    discussion.assessment_id = data.get('assessment_id', discussion.assessment_id)
    discussion.user_type = data.get('user_type', discussion.user_type)
    discussion.student_id = data.get('student_id', discussion.student_id)
    discussion.tm_id = data.get('tm_id', discussion.tm_id)
    discussion.comment = data.get('comment', discussion.comment)
    db.session.commit()
    return jsonify({'message': 'Discussion updated successfully'}), 200

# ==============================================================================Delete Discussion
@discussion_bp.route('/discussion/<int:discussion_id>', methods=['DELETE'])
@jwt_required()
def delete_discussion(discussion_id):
    discussion = Discussion.query.get_or_404(discussion_id)
    db.session.delete(discussion)
    db.session.commit()
    return jsonify({'message': 'Discussion deleted successfully'}), 200
