from flask import Blueprint, request, jsonify
from models import db, Questions

questions_bp = Blueprint("questions", __name__)

# Get all questions
@questions_bp.route("/questions", methods=["GET"])
def get_questions():
    questions = Questions.query.all()
    return jsonify([
        {
            "id": question.id,
            "assessment_id": question.assessment_id,
            "type": question.type,
            "question_text": question.question_text,
            "options": question.options,
            "correct_answer": question.correct_answer,
        }
        for question in questions
    ])

# Get a specific question by ID
@questions_bp.route("/questions/<int:id>", methods=["GET"])
def get_question(id):
    question = Questions.query.get(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404
    return jsonify({
        "id": question.id,
        "assessment_id": question.assessment_id,
        "type": question.type,
        "question_text": question.question_text,
        "options": question.options,
        "correct_answer": question.correct_answer,
    })

# Create a new question
@questions_bp.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    new_question = Questions(
        assessment_id=data.get("assessment_id"),
        type=data.get("type"),
        question_text=data.get("question_text"),
        options=data.get("options"),
        correct_answer=data.get("correct_answer"),
    )
    db.session.add(new_question)
    db.session.commit()

    return jsonify({"message": "Question created successfully", "id": new_question.id}), 201

# Update a question
@questions_bp.route("/questions/<int:id>", methods=["PATCH"])
def update_question(id):
    question = Questions.query.get(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()
    question.assessment_id = data.get("assessment_id", question.assessment_id)
    question.type = data.get("type", question.type)
    question.question_text = data.get("question_text", question.question_text)
    question.options = data.get("options", question.options)
    question.correct_answer = data.get("correct_answer", question.correct_answer)

    db.session.commit()
    return jsonify({"message": "Question updated successfully"})

# Delete a question
@questions_bp.route("/questions/<int:id>", methods=["DELETE"])
def delete_question(id):
    question = Questions.query.get(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully"}), 200
