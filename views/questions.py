from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Questions

questions_bp = Blueprint("questions", __name__)

#fetch all questions according assessment
@questions_bp.route("/questions/<int:assessment_id>", methods=["GET"])
@jwt_required()
def get_questions(assessment_id):
    # Fetch questions that belong to the given assessment_id
    questions = Questions.query.filter_by(assessment_id=assessment_id).all()

    return jsonify([
        {
            "id": question.id,
            "assessment_id": question.assessment_id,
            "question_text": question.question_text,
            "choices": {
                "A": question.choice_a,
                "B": question.choice_b,
                "C": question.choice_c,
                "D": question.choice_d
            },
            "correct_answer": question.correct_answer
        }
        for question in questions
    ])


# Get a single question by ID
@questions_bp.route("/question/<int:id>", methods=["GET"])
@jwt_required()
def get_question(id):
    question = Questions.query.get(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    return jsonify({
        "id": question.id,
        "assessment_id": question.assessment_id,
        "question_text": question.question_text,
        "choices": {
            "A": question.choice_a,
            "B": question.choice_b,
            "C": question.choice_c,
            "D": question.choice_d
        },
        "correct_answer": question.correct_answer
    })

@questions_bp.route("/questions", methods=["POST"])
@jwt_required()
def create_question():
    data = request.get_json()

    required_fields = ["assessment_id", "question_text", "choice_a", "choice_b", "choice_c", "choice_d", "correct_answer"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_question = Questions(
        assessment_id=data["assessment_id"],
        question_text=data["question_text"],
        choice_a=data["choice_a"],
        choice_b=data["choice_b"],
        choice_c=data["choice_c"],
        choice_d=data["choice_d"],
        correct_answer=data["correct_answer"]
    )

    db.session.add(new_question)
    db.session.commit()

    return jsonify({"message": "Question created successfully", "id": new_question.id}), 201

# Update a question
@questions_bp.route("/questions/<int:id>", methods=["PATCH"])
@jwt_required()
def update_question(id):
    question = Questions.query.get(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()

    question.assessment_id = data.get("assessment_id", question.assessment_id)
    question.question_text = data.get("question_text", question.question_text)
    question.choice_a = data.get("choice_a", question.choice_a)
    question.choice_b = data.get("choice_b", question.choice_b)
    question.choice_c = data.get("choice_c", question.choice_c)
    question.choice_d = data.get("choice_d", question.choice_d)
    question.correct_answer = data.get("correct_answer", question.correct_answer)

    db.session.commit()

    return jsonify({"message": "Question updated successfully"})

# Delete a question
@questions_bp.route("/questions/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_question(id):
    question = Questions.query.get(id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200
