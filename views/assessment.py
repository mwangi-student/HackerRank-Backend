from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Assessment
from flask_jwt_extended import jwt_required, get_jwt_identity


assessment_bp = Blueprint('assessment_bp', __name__)

# Fetch all assessments
@assessment_bp.route('/assessment', methods=['GET'])
@jwt_required()
def get_assessments():
    assessments = Assessment.query.all()
    result = [
        {
            'id': assessment.id,
            'title': assessment.title,
            'description': assessment.description,
            'difficulty': assessment.difficulty,
            'category': assessment.category,
            'constraints': assessment.constraints,
            'tm_id': assessment.tm_id,
            'created_at': assessment.created_at
 
        } for assessment in assessments
    ]
    return jsonify(result)

# Fetch a single assessment by ID
@assessment_bp.route('/assessment/<int:id>', methods=['GET'])
@jwt_required()
def get_assessment(id):
    assessment = Assessment.query.get_or_404(id)

    # Get the logged-in TM's ID from JWT
    tm_id = get_jwt_identity()

    result = {
        'id': assessment.id,
        'title': assessment.title,
        'description': assessment.description,
        'difficulty': assessment.difficulty,
        'category': assessment.category,
        'constraints': assessment.constraints,
        'tm_id': tm_id,
        'created_at': assessment.created_at
    }
    return jsonify(result)


# Create a new assessment
@assessment_bp.route('/assessment', methods=['POST'])
@jwt_required()
def create_assessment():
    data = request.get_json()
    
    # Get the logged-in TM's ID from JWT
    tm_id = get_jwt_identity()

    new_assessment = Assessment(
        title=data['title'],
        description=data['description'],
        difficulty=data['difficulty'],
        category=data['category'],
        constraints=data['constraints'],
        tm_id=tm_id, 
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_assessment)  
    db.session.commit()

    return jsonify({'message': 'Assessment created successfully'}), 201

# Update an existing assessment
@assessment_bp.route('/assessment/<int:id>', methods=['PATCH'])
@jwt_required()
def update_assessment(id):
    data = request.get_json()

    # Get the logged-in TM's ID from JWT
    tm_id = get_jwt_identity()

    assessment = Assessment.query.get_or_404(id)

    assessment.title = data.get('title', assessment.title)
    assessment.description = data.get('description', assessment.description)
    assessment.difficulty = data.get('difficulty', assessment.difficulty)
    assessment.category = data.get('category', assessment.category)
    assessment.constraints = data.get('constraints', assessment.constraints)
    assessment.tm_id = data.get('tm_id', tm_id)

    db.session.commit()  
    return jsonify({'message': 'Assessment updated successfully'})

# Delete an existing assessment
@assessment_bp.route('/assessment/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    db.session.delete(assessment) 
    db.session.commit()
    return jsonify({'message': 'Assessment deleted successfully'})
