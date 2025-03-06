from flask import Blueprint, request, jsonify
from models import db, Scores
from flask_jwt_extended import jwt_required

score_bp = Blueprint('score_bp', __name__)

# Create a new score
@score_bp.route('/scores', methods=['POST'])
@jwt_required()
def create_score():
    data = request.get_json()

    
    if not all(k in data for k in ("student_id", "assessment_id", "score")):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_score = Scores(
            student_id=data["student_id"],
            assessment_id=data["assessment_id"],
            score=data["score"]
        )
        db.session.add(new_score)
        db.session.commit()

        return jsonify({"message": "Score created successfully", "score": {
            "id": new_score.id,
            "student_id": new_score.student_id,
            "assessment_id": new_score.assessment_id,
            "score": new_score.score
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get all scores
@score_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_scores():
    scores = Scores.query.all()
    scores_list = [
        {
            "id": score.id,
            "student_id": score.student_id,
            "assessment_id": score.assessment_id,
            "score": score.score
        }
        for score in scores
    ]
    return jsonify(scores_list), 200

# Get a single score by ID
@score_bp.route('/scores/<int:id>', methods=['GET'])
@jwt_required()
def get_score(id):
    score = Scores.query.get(id)
    if not score:
        return jsonify({"error": "Score not found"}), 404

    return jsonify({
        "id": score.id,
        "student_id": score.student_id,
        "assessment_id": score.assessment_id,
        "score": score.score
    }), 200
