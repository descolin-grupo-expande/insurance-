from flask import Blueprint, request, jsonify
from app.extensions import db
from app import models as m

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(m.User)).scalars().all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.execute(db.select(m.User).where(m.User.id == user_id)).scalar()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.execute(db.select(m.User).where(m.User.id == user_id)).scalar()
    data = request.get_json()
    user.username = data['username']
    user.email = data['email']
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = m.User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username, 'email': new_user.email}), 201