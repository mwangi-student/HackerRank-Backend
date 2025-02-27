from flask import Blueprint, request, jsonify
from models import db, Feedback, TM, Student
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message


feedback_bp = Blueprint("feedback", __name__)

# Get all feedback
@feedback_bp.route("/feedback", methods=["GET"])
@jwt_required()
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
@jwt_required()
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

#======================================================================= Create new feedback
@feedback_bp.route("/feedback", methods=["POST"])
@jwt_required()
def create_feedback():

    from flask_mail import mail

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    question_id = data.get("question_id")
    student_id = data.get("student_id")
    tm_id = data.get("tm_id")
    feedback_text = data.get("feedback")

    # Identify the user making the request
    current_user = get_jwt_identity()  # This should return user ID
    
    # Fetch student and TM details
    student = Student.query.get(student_id)
    tm = TM.query.get(tm_id)

    if not student or not tm:
        return jsonify({"error": "Invalid student or TM ID"}), 400

    # Create feedback entry
    new_feedback = Feedback(
        question_id=question_id,
        student_id=student_id,
        tm_id=tm_id,
        feedback=feedback_text
    )
    db.session.add(new_feedback)
    db.session.commit()

    # Determine recipient based on who created the feedback
    try:
        if current_user == student_id:  # Student created the feedback
            recipient_email = tm.email
            recipient_name = tm.username
            sender_name = student.username
        elif current_user == tm_id:  # TM created the feedback
            recipient_email = student.email
            recipient_name = student.username
            sender_name = tm.username
        else:
            return jsonify({"error": "Unauthorized"}), 403

        # Send Email Notification
        msg = Message('New Feedback Notification', recipients=[recipient_email])
        msg.body = f"""
        Hello {recipient_name},

        A new feedback has been created for you by {sender_name}.

        Feedback Details:
        - Question ID: {question_id}
        - Feedback: {feedback_text}

        Please review the feedback at your earliest convenience.

        Regards,
        Admin Team
        """
        mail.send(msg)

    except Exception as e:
        return jsonify({'message': 'Feedback created, but email sending failed', 'error': str(e)}), 500

    return jsonify({"message": "Feedback created successfully, email sent", "id": new_feedback.id}), 201

# ============================================================================Update feedback
@feedback_bp.route("/feedback/<int:id>", methods=["PATCH"])
@jwt_required()
def update_feedback(id):
    feedback = Feedback.query.get(id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404

    data = request.get_json()
    feedback.feedback = data.get("feedback", feedback.feedback)

    db.session.commit()
    return jsonify({"message": "Feedback updated successfully"})

#============================================================================= Delete feedback
@feedback_bp.route("/feedback/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_feedback(id):
    feedback = Feedback.query.get(id)
    if not feedback:
        return jsonify({"error": "Feedback not found"}), 404

    db.session.delete(feedback)
    db.session.commit()
    return jsonify({"message": "Feedback deleted successfully"}), 200
