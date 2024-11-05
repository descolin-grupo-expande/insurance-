from flask import Blueprint, request, jsonify
from app.extensions import db
from app import models as m
from app.config import config
import jwt
from jwt import (
    ExpiredSignatureError, InvalidSignatureError, InvalidAudienceError,
    ImmatureSignatureError, InvalidIssuerError, DecodeError, InvalidTokenError, encode, decode
)
from flask import Flask, request, jsonify, redirect, make_response, url_for
from datetime import datetime, timedelta
from functools import wraps


auth_bp = Blueprint('auth_bp', __name__)

database = {
    "users": [{"national_id":"2493051190101", "email":"psantos@grupoexpande.com"}]  # Stores user data as dictionaries
}

def find_user_by_national_id(national_id):
    return next((user for user in database["users"] if user["national_id"] == national_id), None)

def create_user(email, insurance_id, national_id):
    user = {"email": email, "insurance_id": insurance_id, "national_id": national_id}
    database["users"].append(user)
    return user

def generate_jwt(user):
    payload = {
        "sub": user["national_id"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    token = encode(payload, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('session_token')
        print(token)
        if not token:
            return jsonify({"error": "Authentication token is missing"}), 401
        try:
            data = decode(token, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
            user = find_user_by_national_id(data['sub'])
            if not user:
                return jsonify({"error": "User not found"}), 401
            # Attach user information to the request context
            request.user = user
        except ExpiredSignatureError:
            return jsonify({"error": "Session token has expired"}), 401
        except InvalidTokenError:
            return jsonify({"error": "Invalid session token"}), 401
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/', methods=['POST'])
def authenticate_user():
    # Company B sends a one-time token and user details in the POST request
    one_time_token = request.json.get("one_time_token")
    email = request.json.get("email")
    national_id = request.json.get("national_id")
    #insurance_id = request.json.get("insurance_id")
    
    if not all([one_time_token, email, national_id]):
        return jsonify({"error": "Missing one-time token or user details"}), 400

    try:
        print('decode')
        print(one_time_token)
        # Verify the one-time token (could be implemented with its own secret and expiry)
        var = decode(one_time_token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        print(var)
        # Check if the user exists in Company A's database, create if necessary
        user = find_user_by_national_id(national_id)
        if not user:
            #user = create_user(email, insurance_id, national_id)
            user = create_user(email, national_id)

        # Generate a session token for Company A and set it as an HttpOnly cookie
        session_token = generate_jwt(user)
        response = make_response()
        response.set_cookie(
            "session_token",
            session_token,
            httponly=True,
            secure=True,  # Ensure this is True in production (requires HTTPS)
            samesite="Strict",
            max_age=3600  # 1 hour in seconds
        )

        # Redirect back to Company B’s mobile app without the session token in the URL
        redirect_url = "https://session-dot-frontend-dot-insurance-portal-dev.uc.r.appspot.com/"
        response.headers["Location"] = redirect_url
        response.headers["Cache-Control"] = "private"
        response.status_code = 307
        return response

    except ExpiredSignatureError:
        return jsonify({"error": "One-time token has expired"}), 400
    except InvalidTokenError:
        return jsonify({"error": "Invalid one-time token"}), 400

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route():
    user = request.user
    return jsonify({
        "message": f"Hello, {user['email']}!",
        "user": {
            "email": user["email"],
            "national_id": user["national_id"]
        }
    }), 200

@auth_bp.route('/public', methods=['GET'])
#@token_required
def public_route():
    return jsonify({
        "message": f"Hello, public!",
        "user": {
            "email": "",
            "national_id": ""
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.set_cookie('session_token', '', expires=0)
    return response, 200