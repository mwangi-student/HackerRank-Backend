from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, TM
from flask_mail import Message
from flask_jwt_extended import jwt_required
from flask import current_app



# Blueprint setup
tm_bp = Blueprint('tm', __name__)

#===================================================== create TM
@tm_bp.route('/tm', methods=['POST'])
@jwt_required()
def create_tm():


    data = request.get_json()
    
    password = data.get('password')  
    if not password:
        return jsonify({'error': 'Password is required'}), 400  
    
    hashed_password = generate_password_hash(password)  

    new_tm = TM(
        username=data.get('username'),
        email=data.get('email'),
        password=hashed_password  
    )
    
    db.session.add(new_tm)
    db.session.commit()

     # Sending Email
    try:
        mail = current_app.extensions['mail'] 
        msg = Message('Your TM Account Details', recipients=[new_tm.email])
        msg.body = f"Hello {new_tm.username},\n\nYour account has been created successfully.\n\nUsername: {new_tm.email}\nPassword: {password}\n\nPlease keep your credentials safe."
        mail.send(msg)
    except Exception as e:
        return jsonify({'message': 'TM created, but email sending failed', 'error': str(e)}), 500

    return jsonify({'message': 'TM created successfully, email sent'}), 201
    


#============================================================ Read all TMs
@tm_bp.route('/tm', methods=['GET'])
@jwt_required()
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

# =====================================================Read single TM
@tm_bp.route('/tm/<int:tm_id>', methods=['GET'])
@jwt_required()
def get_tm(tm_id):
    tm = TM.query.get_or_404(tm_id)
    return jsonify({
        'id': tm.id,
        'username': tm.username,
        'email': tm.email,
        'created_at': tm.created_at
    }), 200

# ===================================================================Update TM
@tm_bp.route('/tm/<int:tm_id>', methods=['PATCH'])
@jwt_required()
def update_tm(tm_id):
    tm = TM.query.get_or_404(tm_id)
    data = request.get_json()
    
    tm.username = data.get('username', tm.username)
    tm.email = data.get('email', tm.email)
    
    if 'password' in data:
        tm.password = generate_password_hash(data['password'])
    
    db.session.commit()
    return jsonify({'message': 'TM updated successfully'}), 200

#======================================================================= Delete TM
@tm_bp.route('/tm/<int:tm_id>', methods=['DELETE'])
@jwt_required()
def delete_tm(tm_id):
    tm = TM.query.get_or_404(tm_id)
    db.session.delete(tm)
    db.session.commit()
    return jsonify({'message': 'TM deleted successfully'}), 200