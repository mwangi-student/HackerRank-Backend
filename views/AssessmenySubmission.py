from flask import Blueprint, jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required
from sqlalchemy import not_
from sqlalchemy.orm import joinedload  # Correct import
from collections import OrderedDict
from models import AssessmentSubmission, Assessment, Student, db, MCQSubmission, CodeSubmission

submission_bp = Blueprint('submission', __name__)

@submission_bp.route("/submission", methods=["GET"])
@jwt_required()
def get_submissions():
    try:
        # Fetch all submissions without filtering
        submissions = (
            db.session.query(
                AssessmentSubmission,
                Student.username.label("student_username"),
                Assessment.assessment_type,
                Assessment.title.label("assessment_title"),
            )
            .outerjoin(Student, AssessmentSubmission.student_id == Student.id)  # Left join to avoid filtering out missing students
            .outerjoin(Assessment, AssessmentSubmission.assessment_id == Assessment.id)  # Left join to avoid filtering out missing assessments
            .options(joinedload(AssessmentSubmission.mcq_submissions))
            .options(joinedload(AssessmentSubmission.code_submission))
            .all()
        )

        print(f"Fetched Submissions: {len(submissions)}")

        submissions_list = []
        student_dict = OrderedDict()

        for submission, student_username, assessment_type, assessment_title in submissions:
            submission_data = {
                "id": submission.id,
                "student_id": submission.student_id,
                "student_username": student_username if student_username else "Unknown",  # Handle missing students
                "assessment_id": submission.assessment_id,
                "submitted_at": submission.submitted_at.isoformat() if submission.submitted_at else None,
                "assessment_type": assessment_type if assessment_type else "Unknown",  # Handle missing assessments
                "assessment_title": assessment_title if assessment_title else "Untitled",
                "mcq_answers": [
                    {"question_id": mcq.question_id, "selected_answer": mcq.selected_answer}
                    for mcq in submission.mcq_submissions
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

            # Store unique students
            if submission.student_id not in student_dict:
                student_dict[submission.student_id] = {
                    "student_id": submission.student_id,
                    "student_username": student_username if student_username else "Unknown",
                }

        print(f"Returning {len(submissions_list)} submissions and {len(student_dict)} students.")

        return jsonify({
            "submissions": submissions_list,
            "students": list(student_dict.values())
        })

    except Exception as e:
        print(f"Error fetching submissions: {e}")
        return jsonify({"error": "An error occurred while fetching submissions"}), 500


# Create a new submission
@submission_bp.route("/submission", methods=["POST"])
@jwt_required()
def create_submission():
    data = request.get_json()

    # Validate required fields
    required_fields = ["student_id", "assessment_id", "assessment_type", "assessment_title"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # Create new submission record
    new_submission = AssessmentSubmission(
        student_id=data["student_id"],
        assessment_id=data["assessment_id"],
        assessment_type=data["assessment_type"],
        assessment_title=data["assessment_title"],
        submitted_at=datetime.utcnow()
    )
    db.session.add(new_submission)
    db.session.commit()  # Commit first to get new_submission.id

    # Save MCQ submissions if provided
    if "mcq_answers" in data and isinstance(data["mcq_answers"], list):
        for mcq in data["mcq_answers"]:
            if "question_id" not in mcq or "selected_answer" not in mcq:
                return jsonify({"error": "Invalid MCQ submission format"}), 400

            mcq_submission = MCQSubmission(
                assessment_submission_id=new_submission.id,
                question_id=mcq["question_id"],
                selected_answer=mcq["selected_answer"]
            )
            db.session.add(mcq_submission)

    # Save Code Submission if provided
    if "code_submission" in data and isinstance(data["code_submission"], dict):
        if "codechallenge_id" not in data["code_submission"] or "selected_answer" not in data["code_submission"]:
            return jsonify({"error": "Invalid Code Submission format"}), 400

        code_submission = CodeSubmission(
            assessment_submission_id=new_submission.id,
            codechallenge_id=data["code_submission"]["codechallenge_id"],
            selected_answer=data["code_submission"]["selected_answer"]
        )
        db.session.add(code_submission)

    db.session.commit()  # Final commit

    return jsonify({
        "message": "Submission created successfully",
        "submission": new_submission.to_dict()
    }), 201


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
