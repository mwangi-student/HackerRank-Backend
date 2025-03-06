from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, MCQSubmission
from flask_jwt_extended import jwt_required

mcqsubmission_bp = Blueprint('mcqsubmission_bp', __name__)

@mcqsubmission_bp.route("/mcq-submissions", methods=["GET"])
@jwt_required()
def get_all_mcq_submissions():
    submissions = MCQSubmission.query.all()
    return jsonify([
        {"id": sub.id, "assessment_submission_id": sub.submission_id, "question_id": sub.question_id, "selected_answer": sub.selected_answer}
        for sub in submissions
    ])
@mcqsubmission_bp.route("/mcq-submissions/<int:submission_id>", methods=["GET"])
def get_mcq_submission(submission_id):
    submission = MCQSubmission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "MCQ Submission not found"}), 404
    return jsonify({"id": submission.id, "assessment_submission_id": submission.submission_id, "question_id": submission.question_id, "selected_answer": submission.selected_answer})

@mcqsubmission_bp.route("/mcq-submissions", methods=["POST"])
@jwt_required()
def create_mcq_submission():
    data = request.json
    new_submission = MCQSubmission(
        assessment_submission_id=data["assessment_submission_id"],
        question_id=data["question_id"],
        selected_answer=data["selected_answer"]
    )
    db.session.add(new_submission)
    db.session.commit()
    return jsonify({"message": "MCQ Submission created", "id": new_submission.id}), 201

