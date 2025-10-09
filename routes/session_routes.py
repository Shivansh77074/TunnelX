"""
Session API Routes for SecureSession
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import asyncio

session_bp = Blueprint('sessions', __name__)

@session_bp.route('/', methods=['POST'])
@jwt_required()
def create_session():
    """Create a new secure session."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        recipient_email = data.get('recipient_email')
        duration_hours = data.get('duration_hours', 1)

        if not recipient_email:
            return jsonify({'error': 'Recipient email required'}), 400

        if duration_hours > 24:  # MAX_SESSION_DURATION
            return jsonify({'error': 'Maximum session duration is 24 hours'}), 400

        # Create session
        session_service = current_app.session_service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(
                session_service.create_session(user_id, recipient_email, duration_hours)
            )
        finally:
            loop.close()

        return jsonify({
            'message': 'Session created successfully',
            'session': result
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Session creation failed'}), 500

@session_bp.route('/<session_id>/messages', methods=['GET'])
@jwt_required()
def get_messages(session_id):
    """Get messages for a session."""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 50, type=int)

        session_service = current_app.session_service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            messages = loop.run_until_complete(
                session_service.get_session_messages(session_id, user_id, limit)
            )
        finally:
            loop.close()

        return jsonify({
            'messages': messages,
            'count': len(messages)
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': 'Failed to get messages'}), 500

@session_bp.route('/<session_id>/messages', methods=['POST'])
@jwt_required()
def send_message(session_id):
    """Send a message in a session."""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        message = data.get('message')
        message_type = data.get('type', 'text')

        if not message:
            return jsonify({'error': 'Message content required'}), 400

        session_service = current_app.session_service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(
                session_service.send_message(session_id, user_id, message, message_type)
            )
        finally:
            loop.close()

        return jsonify({
            'message': 'Message sent successfully',
            'result': result
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 403
    except Exception as e:
        return jsonify({'error': 'Failed to send message'}), 500

@session_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_sessions():
    """Get all sessions for the current user."""
    try:
        user_id = get_jwt_identity()

        session_service = current_app.session_service
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            sessions = loop.run_until_complete(
                session_service.get_user_sessions(user_id)
            )
        finally:
            loop.close()

        return jsonify({
            'sessions': sessions,
            'count': len(sessions)
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to get sessions'}), 500
