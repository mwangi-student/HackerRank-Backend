from flask import Blueprint, request, jsonify
from models import db, TM

# Blueprint setup
tm_bp = Blueprint('tm', __name__)

# Create TM
@tm_bp.route('/tm', methods=['POST'])
def create_tm():
    data = request.get_json()
    new_tm = TM(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password')
    )
    db.session.add(new_tm)
    db.session.commit()
    return jsonify({'message': 'TM created successfully'}), 201

# Read all TMs
@tm_bp.route('/tm', methods=['GET'])
def get_all_tms():
    tms = TM.query.all()
    result = []
    for tm in tms:
        result.append({
            'id': tm.id,
            'username': tm.username,
            'email': tm.email,
            'created_at': tm.created_at
        })
    return jsonify(result), 200

# Read single TM
@tm_bp.route('/tm/<int:tm_id>', methods=['GET'])
def get_tm(tm_id):
    tm = TM.query.get_or_404(tm_id)
    return jsonify({
        'id': tm.id,
        'username': tm.username,
        'email': tm.email,
        'created_at': tm.created_at
    }), 200

# Update TM
@tm_bp.route('/tm/<int:tm_id>', methods=['PUT'])
def update_tm(tm_id):
    tm = TM.query.get_or_404(tm_id)
    data = request.get_json()
    tm.username = data.get('username', tm.username)
    tm.email = data.get('email', tm.email)
    tm.password = data.get('password', tm.password)
    db.session.commit()
    return jsonify({'message': 'TM updated successfully'}), 200

# Delete TM
@tm_bp.route('/tm/<int:tm_id>', methods=['DELETE'])
def delete_tm(tm_id):
    tm = TM.query.get_or_404(tm_id)
    db.session.delete(tm)
    db.session.commit()
    return jsonify({'message': 'TM deleted successfully'}), 200