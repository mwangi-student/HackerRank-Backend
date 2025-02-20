from flask import Blueprint, request, jsonify
from models import db, Leaderboard

leaderboard_bp = Blueprint('leaderboard', __name__)

# Create Leaderboard Entry
@leaderboard_bp.route('/leaderboard', methods=['POST'])
def create_leaderboard():
    data = request.get_json()
    new_entry = Leaderboard(
        student_id=data.get('student_id'),
        assessment_id=data.get('assessment_id'),
        total_score=data.get('total_score'),
        rank=data.get('rank')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Leaderboard entry created successfully'}), 201

# Read All Leaderboard Entries
@leaderboard_bp.route('/leaderboard', methods=['GET'])
def get_all_leaderboard():
    entries = Leaderboard.query.all()
    result = []
    for entry in entries:
        result.append({
            'id': entry.id,
            'student_id': entry.student_id,
            'assessment_id': entry.assessment_id,
            'total_score': entry.total_score,
            'rank': entry.rank,
            'last_updated': entry.last_updated
        })
    return jsonify(result), 200

# # Read Single Leaderboard Entry
# @leaderboard_bp.route('/leaderboard/<int:entry_id>', methods=['GET'])
# def get_leaderboard(entry_id):
#     entry = Leaderboard.query.get_or_404(entry_id)
#     return jsonify({
#         'id': entry.id,
#         'student_id': entry.student_id,
#         'assessment_id': entry.assessment_id,
#         'total_score': entry.total_score,
#         'rank': entry.rank,
#         'last_updated': entry.last_updated
#     }), 200

# Update Leaderboard Entry
@leaderboard_bp.route('/leaderboard/<int:entry_id>', methods=['PUT'])
def update_leaderboard(entry_id):
    entry = Leaderboard.query.get_or_404(entry_id)
    data = request.get_json()
    entry.student_id = data.get('student_id', entry.student_id)
    entry.assessment_id = data.get('assessment_id', entry.assessment_id)
    entry.total_score = data.get('total_score', entry.total_score)
    entry.rank = data.get('rank', entry.rank)
    db.session.commit()
    return jsonify({'message': 'Leaderboard entry updated successfully'}), 200

# Delete Leaderboard Entry
@leaderboard_bp.route('/leaderboard/<int:entry_id>', methods=['DELETE'])
def delete_leaderboard(entry_id):
    entry = Leaderboard.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Leaderboard entry deleted successfully'}), 200