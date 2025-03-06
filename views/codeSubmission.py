from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, CodeSubmission
from flask_jwt_extended import jwt_required

codesubmission_bp = Blueprint('codesubmission_bp', __name__)

@codesubmission_bp.route("/code-submissions", methods=["GET"])
@jwt_required()
def get_all_code_submissions():
    submissions = CodeSubmission.query.all()
    return jsonify([
        {"id": sub.id, "submission_id": sub.submission_id, "codechallenge_id": sub.codechallenge_id, "selected_answer": sub.selected_answer}
        for sub in submissions
    ])

@codesubmission_bp.route("/code-submissions/<int:submission_id>", methods=["GET"])
def get_code_submission(submission_id):
    submission = CodeSubmission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "Code Submission not found"}), 404
    return jsonify({"id": submission.id, "submission_id": submission.submission_id, "codechallenge_id": submission.codechallenge_id, "selected_answer": submission.selected_answer})


@codesubmission_bp.route("/code-submissions", methods=["POST"])
@jwt_required()
def create_code_submission():
    data = request.json
    new_submission = CodeSubmission(
    assessment_submission_id=data["assessment_submission_id"],  # ✅ Correct key
    codechallenge_id=data["codechallenge_id"],
    selected_answer=data["selected_answer"]
    )
    db.session.add(new_submission)
    db.session.commit()
    return jsonify({"message": "Code Submission created", "id": new_submission.id}), 201
