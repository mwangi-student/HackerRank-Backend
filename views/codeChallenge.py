from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, CodeChallenge

code_challenge_bp = Blueprint('code_challenge_bp', __name__)

# create-challenge
@code_challenge_bp.route('/code-challenges', methods=['POST'])
@jwt_required()
def create_code_challenge():
    data = request.get_json()

    required_fields = [
        "assessment_id", "task", "example", "input_format", 
        "output_format", "constraints", "sample_input", "sample_output_1", "sample_output_2", "sample_output_3", "sample_output_4"
    ]
    
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_challenge = CodeChallenge(
        assessment_id=data["assessment_id"],
        task=data["task"],
        example=data["example"],
        input_format=data["input_format"],
        output_format=data["output_format"],
        constraints=data["constraints"],
        sample_input=data["sample_input"],
        sample_output_1=data["sample_output_1"],
        sample_output_2=data["sample_output_2"],
        sample_output_3=data["sample_output_3"],
        sample_output_4=data["sample_output_4"]
    )

    db.session.add(new_challenge)
    db.session.commit()

    return jsonify({"message": "Code Challenge created successfully", "id": new_challenge.id}), 201


# fetching all code challenges
@code_challenge_bp.route('/code-challenges', methods=['GET'])
@jwt_required()
def get_all_code_challenges():
    challenges = CodeChallenge.query.all()
    
    result = [
        {
            "id": challenge.id,
            "assessment_id": challenge.assessment_id,
            "task": challenge.task,
            "example": challenge.example,
            "input_format": challenge.input_format,
            "output_format": challenge.output_format,
            "constraints": challenge.constraints,
            "sample_input": challenge.sample_input,
            "sample_output_1": challenge.sample_output,
            "sample_output_2": challenge.sample_output,
            "sample_output_3": challenge.sample_output,
            "sample_output_4": challenge.sample_output
        }
        for challenge in challenges
    ]
    
    return jsonify(result)

# fetch a single code challenge
@code_challenge_bp.route('/code-challenges/<int:id>', methods=['GET'])
@jwt_required()
def get_code_challenge(id):
    challenge = CodeChallenge.query.get_or_404(id)
    
    result = {
        "id": challenge.id,
        "assessment_id": challenge.assessment_id,
        "task": challenge.task,
        "example": challenge.example,
        "input_format": challenge.input_format,
        "output_format": challenge.output_format,
        "constraints": challenge.constraints,
        "sample_input": challenge.sample_input,
        "sample_output_1": challenge.sample_output,
        "sample_output_2": challenge.sample_output,
        "sample_output_3": challenge.sample_output,
        "sample_output_4": challenge.sample_output
    }
    
    return jsonify(result)
#  update a  single code challenge
@code_challenge_bp.route('/code-challenges/<int:id>', methods=['PATCH'])
@jwt_required()
def update_code_challenge(id):
    challenge = CodeChallenge.query.get_or_404(id)
    data = request.get_json()

    challenge.assessment_id = data.get("assessment_id", challenge.assessment_id)
    challenge.task = data.get("task", challenge.task)
    challenge.example = data.get("example", challenge.example)
    challenge.input_format = data.get("input_format", challenge.input_format)
    challenge.output_format = data.get("output_format", challenge.output_format)
    challenge.constraints = data.get("constraints", challenge.constraints)
    challenge.sample_input = data.get("sample_input", challenge.sample_input)
    challenge.sample_output_1 = data.get("sample_output", challenge.sample_output)
    challenge.sample_output_2 = data.get("sample_output", challenge.sample_output)
    challenge.sample_output_3 = data.get("sample_output", challenge.sample_output)
    challenge.sample_output_4 = data.get("sample_output", challenge.sample_output)

    db.session.commit()

    return jsonify({"message": "Code Challenge updated successfully"})


# delete a code challenge
@code_challenge_bp.route('/code-challenges/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_code_challenge(id):
    challenge = CodeChallenge.query.get_or_404(id)
    
    db.session.delete(challenge)
    db.session.commit()

    return jsonify({"message": "Code Challenge deleted successfully"})
