from flask import Blueprint, request, jsonify
from models import db, Submission

submission_bp = Blueprint("submission", __name__)

# Get all submissions
@submission_bp.route("/submission", methods=["GET"])
def get_submissions():
    submissions = Submission.query.all()
    return jsonify([
        {
            "id": submission.id,
            "student_id": submission.student_id,
            "question_id": submission.question_id,
            "assessment_id": submission.assessment_id,
            "answer": submission.answer,
            "status": submission.status,
            "score": submission.score,
            "created_at": submission.created_at
        }
        for submission in submissions
    ])

# Get a single submission by ID
@submission_bp.route("/submission/<int:id>", methods=["GET"])
def get_submission(id):
    submission = Submission.query.get(id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    return jsonify({
        "id": submission.id,
        "student_id": submission.student_id,
        "question_id": submission.question_id,
        "assessment_id": submission.assessment_id,
        "answer": submission.answer,
        "status": submission.status,
        "score": submission.score,
        "created_at": submission.created_at
    })

# Create a new submission
@submission_bp.route("/submission", methods=["POST"])
def create_submission():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_submission = Submission(
        student_id=data.get("student_id"),
        question_id=data.get("question_id"),
        assessment_id=data.get("assessment_id"),
        answer=data.get("answer"),
        status=data.get("status"),
        score=data.get("score")
    )
    db.session.add(new_submission)
    db.session.commit()

    return jsonify({"message": "Submission created successfully", "id": new_submission.id}), 201

# Update a submission
@submission_bp.route("/submission/<int:id>", methods=["PATCH"])
def update_submission(id):
    submission = Submission.query.get(id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    data = request.get_json()
    submission.answer = data.get("answer", submission.answer)
    submission.status = data.get("status", submission.status)
    submission.score = data.get("score", submission.score)

    db.session.commit()
    return jsonify({"message": "Submission updated successfully"})

# Delete a submission
@submission_bp.route("/submission/<int:id>", methods=["DELETE"])
def delete_submission(id):
    submission = Submission.query.get(id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    db.session.delete(submission)
    db.session.commit()
    return jsonify({"message": "Submission deleted successfully"}), 200
