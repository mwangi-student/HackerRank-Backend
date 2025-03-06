from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required
from sqlalchemy import not_
from sqlalchemy.orm import joinedload  # Correct import
from models import AssessmentSubmission, Assessment, Student, db, MCQSubmission, CodeSubmission

submission_bp = Blueprint('submission', __name__)

@submission_bp.route("/submission", methods=["GET"])
@jwt_required()
def get_submissions():
    submissions = (
        AssessmentSubmission.query
        .join(Assessment, AssessmentSubmission.assessment_id == Assessment.id)
        .join(Student, AssessmentSubmission.student_id == Student.id)
        .filter(AssessmentSubmission.submitted_at.isnot(None))  # Ensure assessment is completed
        .options(joinedload(AssessmentSubmission.student))  # Load the student relationship
        .options(joinedload(AssessmentSubmission.assessment))  # Load the assessment relationship
        .options(joinedload(AssessmentSubmission.mcq_answers))  # Load mcq_answers relationship
        .all()
    )

    submissions_list = []
    for submission in submissions:
        submission_data = {
            "id": submission.id,
            "student_id": submission.student_id,
            "student_username": submission.student.username,  # Access student's username
            "assessment_id": submission.assessment_id,
            "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,  # Format the submission time
            "assessment_type": submission.assessment.assessment_type,  # Access assessment_type
            "assessment_title": submission.assessment.title,  # Access assessment title
            "mcq_answers": [
                {"question_id": mcq.question_id, "selected_answer": mcq.selected_answer}
                for mcq in submission.mcq_answers  # Access mcq_answers
            ],
            "code_submission": (
                {
                    "codechallenge_id": submission.code_submission.codechallenge_id,
                    "selected_answer": submission.code_submission.selected_answer
                }
                if submission.code_submission else None
            )
        }
        submissions_list.append(submission_data)

    return jsonify(submissions_list)

# Create a new submission
@submission_bp.route("/submission", methods=["POST"])
@jwt_required()
def create_submission():
    data = request.get_json()

    # Validate required fields
    if not data or "student_id" not in data or "assessment_id" not in data:
        return jsonify({"error": "Missing required fields: student_id, assessment_id"}), 400

    # Create new submission record
    new_submission = AssessmentSubmission(
        student_id=data["student_id"],
        assessment_id=data["assessment_id"],
        submitted_at=datetime.utcnow()
    )
    db.session.add(new_submission)
    db.session.commit()

    # Save MCQ answers if provided
    if "mcq_answers" in data and isinstance(data["mcq_answers"], list):
        for mcq in data["mcq_answers"]:
            if "question_id" not in mcq or "selected_answer" not in mcq:
                return jsonify({"error": "Invalid MCQ submission format"}), 400

            mcq_submission = MCQSubmission(
                submission_id=new_submission.id,
                question_id=mcq["question_id"],
                selected_answer=mcq["selected_answer"]
            )
            db.session.add(mcq_submission)

    # Save Code Submission if provided
    if "code_submission" in data and isinstance(data["code_submission"], dict):
        if "codechallenge_id" not in data["code_submission"] or "selected_answer" not in data["code_submission"]:
            return jsonify({"error": "Invalid Code Submission format"}), 400

        code_submission = CodeSubmission(
            submission_id=new_submission.id,
            codechallenge_id=data["code_submission"]["codechallenge_id"],
            selected_answer=data["code_submission"]["selected_answer"]
        )
        db.session.add(code_submission)

    db.session.commit()

    return jsonify({"message": "Submission created successfully", "id": new_submission.id}), 201

# Delete a submission
@submission_bp.route("/submission/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_submission(id):
    submission = AssessmentSubmission.query.get(id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    # Delete associated MCQ answers
    MCQSubmission.query.filter_by(submission_id=id).delete()
    # Delete associated Code Submission
    CodeSubmission.query.filter_by(submission_id=id).delete()

    db.session.delete(submission)
    db.session.commit()
    return jsonify({"message": "Submission deleted successfully"}), 200
