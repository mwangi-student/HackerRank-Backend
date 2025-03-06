from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, CodeChallenge

code_challenge_bp = Blueprint('code_challenge_bp', __name__)

# create-challenge

@code_challenge_bp.route("/code-challenges", methods=["POST"])
def create_code_challenge():
    try:
        data = request.get_json()
        print("Received data:", data)  # Log the received data

        # Validate required fields
        required_fields = [
            "assessment_id", "task", "example", "input_format", "output_format",
            "constraints", "sample_input_1", "sample_input_2", "sample_input_3",
            "sample_input_4", "sample_output_1", "sample_output_2", "sample_output_3",
            "sample_output_4"
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Process the data (e.g., save to database)
        # Replace this with your actual logic
        print("Saving code challenge:", data)

        return jsonify({"message": "Code challenge created successfully"}), 201
    except Exception as e:
        print("Error creating code challenge:", str(e))  # Log the error
        return jsonify({"error": "Internal server error"}), 500
    
    
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
            "sample_output": challenge.sample_output
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
        "sample_output": challenge.sample_output
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
    challenge.sample_output = data.get("sample_output", challenge.sample_output)

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
