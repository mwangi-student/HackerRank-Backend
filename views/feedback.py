from flask import Blueprint, request, jsonify
from models import db, Feedback

feedback_bp = Blueprint("feedback", __name__)

# Get all feedback
@feedback_bp.route("/feedback", methods=["GET"])
def get_feedback():
    feedbacks = Feedback.query.all()
    return jsonify([
        {
            "id": feedback.id,
            "question_id": feedback.question_id,
            "student_id": feedback.student_id,
            "tm_id": feedback.tm_id,
            "feedback": feedback.feedback,
            "created_at": feedback.created_at
        }
        for feedback in feedbacks
    ])

# Get feedback by ID
@feedback_bp.route("/feedback/<int:id>", methods=["GET"])
def get_feedback_by_id(id):
    feedback = Feedback.query.get(id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404
    return jsonify({
        "id": feedback.id,
        "question_id": feedback.question_id,
        "student_id": feedback.student_id,
        "tm_id": feedback.tm_id,
        "feedback": feedback.feedback,
        "created_at": feedback.created_at
    })

# Create new feedback
@feedback_bp.route("/feedback", methods=["POST"])
def create_feedback():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_feedback = Feedback(
        question_id=data.get("question_id"),
        student_id=data.get("student_id"),
        tm_id=data.get("tm_id"),
        feedback=data.get("feedback")
    )
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({"message": "Feedback created successfully", "id": new_feedback.id}), 201

# Update feedback
@feedback_bp.route("/feedback/<int:id>", methods=["PATCH"])
def update_feedback(id):
    feedback = Feedback.query.get(id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404

    data = request.get_json()
    feedback.feedback = data.get("feedback", feedback.feedback)

    db.session.commit()
    return jsonify({"message": "Feedback updated successfully"})

# Delete feedback
@feedback_bp.route("/feedback/<int:id>", methods=["DELETE"])
def delete_feedback(id):
    feedback = Feedback.query.get(id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404

    db.session.delete(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback deleted successfully"}), 200
