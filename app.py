"""
SecureSession Flask Application Factory
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import datetime

from config import Config

# Import route blueprints
from routes.test_routes import test_bp, test_abc_bp
# Future: import other route blueprints like auth_bp, session_bp, file_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'message': 'Token has expired'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'message': 'Invalid token'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'message': 'Authorization token required'}), 401

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Global API prefix
    api_prefix = '/api/v1'

    # Health check endpoint with global prefix
    @app.route(f'{api_prefix}/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
        })

    # Register blueprints with global prefix
    app.register_blueprint(test_bp, url_prefix=api_prefix)
    app.register_blueprint(test_abc_bp)
    # Future: register other blueprints here
    # app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    # app.register_blueprint(session_bp, url_prefix=f'{api_prefix}/sessions')
    # app.register_blueprint(file_bp, url_prefix=f'{api_prefix}/files')

    return app


#<-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# """
# SecureSession Flask Application Factory
# """
# from flask import Flask, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from datetime import datetime

# from config import Config

# # Import route blueprints
# from routes.test_routes import test_bp
# # Future: import other route blueprints like auth_bp, session_bp, file_bp

# def create_app():
#     """Create and configure Flask application"""
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Initialize extensions
#     CORS(app, origins=app.config['CORS_ORIGINS'])
#     jwt = JWTManager(app)

#     # JWT error handlers
#     @jwt.expired_token_loader
#     def expired_token_callback(jwt_header, jwt_payload):
#         return jsonify({'message': 'Token has expired'}), 401

#     @jwt.invalid_token_loader
#     def invalid_token_callback(error):
#         return jsonify({'message': 'Invalid token'}), 401

#     @jwt.unauthorized_loader
#     def missing_token_callback(error):
#         return jsonify({'message': 'Authorization token required'}), 401

#     # Global error handlers
#     @app.errorhandler(400)
#     def bad_request(error):
#         return jsonify({'error': 'Bad request'}), 400

#     @app.errorhandler(404)
#     def not_found(error):
#         return jsonify({'error': 'Resource not found'}), 404

#     @app.errorhandler(500)
#     def internal_error(error):
#         return jsonify({'error': 'Internal server error'}), 500

#     # Health check endpoint
#     @app.route('/api/health', methods=['GET'])
#     def health_check():
#         return jsonify({
#             'status': 'healthy',
#             'timestamp': datetime.utcnow().isoformat(),
#             'version': '1.0.0',
#         })

#     # Register blueprints
#     app.register_blueprint(test_bp)

#     # Future: register other blueprints here
#     # app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     # app.register_blueprint(session_bp, url_prefix='/api/sessions')
#     # app.register_blueprint(file_bp, url_prefix='/api/files')

#     return app


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

# """
# SecureSession Flask Application Factory - Test API Version
# """
# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_socketio import SocketIO
# from flask_jwt_extended import JWTManager
# from datetime import datetime

# from config import Config
# # from services.crypto_service import CryptoService
# # from services.auth_service import AuthService
# # from services.session_service import SessionService
# # from services.face_service import FaceService
# # from routes.auth_routes import auth_bp
# # from routes.session_routes import session_bp
# # from routes.file_routes import file_bp

# # Import connection module
# # from connection import get_mongo_client
# # , get_redis_client

# def create_app():
#     """Create and configure Flask application"""
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Initialize extensions
#     CORS(app, origins=app.config['CORS_ORIGINS'])
#     socketio = SocketIO(app, cors_allowed_origins=app.config['CORS_ORIGINS'])
#     jwt = JWTManager(app)

#     # Initialize database connections
#     # mongo_client = get_mongo_client()
#     # redis_client = get_redis_client()

#     # Store in app context (for future use)
#     # app.mongo_client = mongo_client
#     # app.redis_client = redis_client

#     # JWT error handlers
#     @jwt.expired_token_loader
#     def expired_token_callback(jwt_header, jwt_payload):
#         return jsonify({'message': 'Token has expired'}), 401

#     @jwt.invalid_token_loader
#     def invalid_token_callback(error):
#         return jsonify({'message': 'Invalid token'}), 401

#     @jwt.unauthorized_loader
#     def missing_token_callback(error):
#         return jsonify({'message': 'Authorization token required'}), 401

#     # Global error handlers
#     @app.errorhandler(400)
#     def bad_request(error):
#         return jsonify({'error': 'Bad request'}), 400

#     @app.errorhandler(404)
#     def not_found(error):
#         return jsonify({'error': 'Resource not found'}), 404

#     @app.errorhandler(500)
#     def internal_error(error):
#         return jsonify({'error': 'Internal server error'}), 500

#     # Test API endpoint
#     @app.route('/api/test', methods=['GET'])
#     def test_api():
#         return jsonify({'status': 'success', 'message': 'API is working!'})
    
#     # Test POST API endpoint
#     @app.route('/post/api/test', methods=['POST'])
#     def test_api_post():
#         data = request.get_json()  # get JSON data from request body
#         if not data:
#             return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
        
#         # Print request body to console
#         print("Received POST data:", data)
#         # You can access fields like: data.get('name') or data.get('email')
#         return jsonify({
#             'status': 'success',
#             'message': 'POST API is working!',
#             'received_data': data
#         })

#     # Health check endpoint
#     @app.route('/api/health', methods=['GET'])
#     def health_check():
#         return jsonify({
#             'status': 'healthy',
#             'timestamp': datetime.utcnow().isoformat(),
#             'version': '1.0.0',
#             # 'database': 'connected' if mongo_client else 'disconnected',
#             # 'cache': 'connected' if redis_client else 'disconnected'
#         })

#     # # Socket.IO events (optional for now)
#     # @socketio.on('connect')
#     # def handle_connect():
#     #     print(f'Client connected')
#     #     return True

#     # @socketio.on('disconnect')
#     # def handle_disconnect():
#     #     print(f'Client disconnected')

#     return app
# # , socketio
