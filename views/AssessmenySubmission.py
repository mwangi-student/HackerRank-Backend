from flask import Blueprint, request, jsonify
from models import db, AssessmentSubmission, MCQSubmission, CodeSubmission

submission_bp = Blueprint("submission", __name__)

# Get all submissions
@submission_bp.route("/submission", methods=["GET"])
def get_submissions():
    submissions = AssessmentSubmission.query.all()
    return jsonify([
        {
            "id": submission.id,
            "student_id": submission.student_id,
            "assessment_id": submission.assessment_id,
            "submitted_at": submission.submitted_at,
            "mcq_answers": [
                {"question_id": mcq.question_id, "selected_answer": mcq.selected_answer}
                for mcq in submission.mcq_answers
            ],
            "code_submission": (
                {"question_id": submission.code_submission.question_id, "selected_answer": submission.code_submission.selected_answer}
                if submission.code_submission else None
            )
        }
        for submission in submissions
    ])

# Get a single submission by ID
@submission_bp.route("/submission/<int:id>", methods=["GET"])
def get_submission(id):
    submission = AssessmentSubmission.query.get(id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404
    return jsonify({
        "id": submission.id,
        "student_id": submission.student_id,
        "assessment_id": submission.assessment_id,
        "submitted_at": submission.submitted_at,
        "mcq_answers": [
            {"question_id": mcq.question_id, "selected_answer": mcq.selected_answer}
            for mcq in submission.mcq_answers
        ],
        "code_submission": (
            {"question_id": submission.code_submission.question_id, "selected_answer": submission.code_submission.selected_answer}
            if submission.code_submission else None
        )
    })

# Create a new submission
@submission_bp.route("/submission", methods=["POST"])
def create_submission():
    data = request.get_json()
    if not data or "student_id" not in data or "assessment_id" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_submission = AssessmentSubmission(
        student_id=data["student_id"],
        assessment_id=data["assessment_id"]
    )
    db.session.add(new_submission)
    db.session.commit()

    # Save MCQ answers if provided
    if "mcq_answers" in data:
        for mcq in data["mcq_answers"]:
            mcq_submission = MCQSubmission(
                submission_id=new_submission.id,
                question_id=mcq["question_id"],
                selected_answer=mcq["selected_answer"]
            )
            db.session.add(mcq_submission)

    # Save Code Submission if provided
    if "code_submission" in data:
        code_submission = CodeSubmission(
            submission_id=new_submission.id,
            question_id=data["code_submission"]["question_id"],
            selected_answer=data["code_submission"]["selected_answer"]
        )
        db.session.add(code_submission)
    
    db.session.commit()
    
    return jsonify({"message": "Submission created successfully", "id": new_submission.id}), 201
