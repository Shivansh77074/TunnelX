"""
Authentication API Routes for SecureSession
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import asyncio

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        username = data['username']
        email = data['email']
        password = data['password']

        # Handle face image if provided
        face_image = None
        if 'face_image' in request.files:
            file = request.files['face_image']
            if file and file.filename:
                face_image = file.read()

        # Register user
        auth_service = current_app.auth_service
        result = auth_service.register_user(username, email, password, face_image)

        return jsonify({
            'message': 'User registered successfully',
            'user': result
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user with credentials."""
    try:
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        # Authenticate user
        auth_service = current_app.auth_service
        result = auth_service.login_user(username, password)

        return jsonify({
            'message': 'Login successful',
            'tokens': {
                'access_token': result['access_token'],
                'refresh_token': result['refresh_token'],
                'expires_in': result['expires_in']
            },
            'user': {
                'user_id': result['user_id'],
                'username': result['username'],
                'public_key': result['public_key'],
                'face_enabled': result['face_enabled']
            }
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/face-verify', methods=['POST'])
@jwt_required()
def verify_face():
    """Verify user identity using face recognition."""
    try:
        user_id = get_jwt_identity()

        if 'face_image' not in request.files:
            return jsonify({'error': 'Face image required'}), 400

        file = request.files['face_image']
        if not file or not file.filename:
            return jsonify({'error': 'Valid face image required'}), 400

        face_image = file.read()

        # Verify face
        auth_service = current_app.auth_service
        is_verified = auth_service.verify_face_authentication(user_id, face_image)

        return jsonify({
            'verified': is_verified,
            'message': 'Face verification successful' if is_verified else 'Face verification failed'
        }), 200

    except Exception as e:
        return jsonify({'error': 'Face verification failed'}), 500

@auth_bp.route('/setup-face', methods=['POST'])
@jwt_required()
def setup_face():
    """Set up face authentication for user."""
    try:
        user_id = get_jwt_identity()

        if 'face_image' not in request.files:
            return jsonify({'error': 'Face image required'}), 400

        file = request.files['face_image']
        if not file or not file.filename:
            return jsonify({'error': 'Valid face image required'}), 400

        face_image = file.read()

        # Setup face authentication
        auth_service = current_app.auth_service
        success = auth_service.setup_face_authentication(user_id, face_image)

        return jsonify({
            'success': success,
            'message': 'Face authentication setup successful' if success else 'Face setup failed'
        }), 200 if success else 400

    except Exception as e:
        return jsonify({'error': 'Face setup failed'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile information."""
    try:
        user_id = get_jwt_identity()

        auth_service = current_app.auth_service
        user_info = auth_service.get_user_info(user_id)

        if not user_info:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': user_info}), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get profile'}), 500
