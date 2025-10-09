# """
# Authentication Service for SecureSession
# Handles user registration, login, JWT tokens, and face recognition
# """
# import uuid
# from datetime import datetime, timedelta
# from typing import Dict, Optional
# from io import BytesIO

# from flask_jwt_extended import create_access_token, create_refresh_token
# import face_recognition
# from PIL import Image

# class AuthService:
#     """Authentication service handling all user authentication needs."""

#     def __init__(self, db, crypto_service):
#         self.db = db
#         self.crypto = crypto_service
#         if self.db:
#             self.users_collection = db.users
#             self.sessions_collection = db.user_sessions
#         else:
#             # Mock collections for development
#             self.users_collection = MockCollection()
#             self.sessions_collection = MockCollection()

#     def register_user(self, username: str, email: str, password: str, 
#                      face_image: Optional[bytes] = None) -> Dict[str, any]:
#         """Register a new user with optional face recognition setup."""

#         # Check if user already exists
#         if self.users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
#             raise ValueError("User already exists with this username or email")

#         # Hash password
#         password_hash = self.crypto.hash_password(password)

#         # Generate RSA keypair for the user
#         keypair = self.crypto.generate_rsa_keypair()

#         # Process face image if provided
#         face_encoding = None
#         if face_image:
#             face_encoding = self._process_face_image(face_image)

#         # Create user document
#         user_data = {
#             'user_id': str(uuid.uuid4()),
#             'username': username,
#             'email': email,
#             'password_hash': password_hash,
#             'public_key': keypair['public_pem'],
#             'private_key': keypair['private_pem'],
#             'face_encoding': face_encoding,
#             'is_active': True,
#             'created_at': datetime.utcnow(),
#             'last_login': None,
#             'failed_login_attempts': 0,
#             'account_locked': False
#         }

#         # Save to database
#         self.users_collection.insert_one(user_data)

#         return {
#             'user_id': user_data['user_id'],
#             'username': username,
#             'email': email,
#             'public_key': keypair['public_pem'],
#             'face_enabled': face_encoding is not None
#         }

#     def login_user(self, username: str, password: str) -> Dict[str, any]:
#         """Authenticate user with username and password."""
#         # Find user
#         user = self.users_collection.find_one({
#             "$or": [{"username": username}, {"email": username}]
#         })

#         if not user:
#             raise ValueError("Invalid credentials")

#         # Check if account is locked
#         if user.get('account_locked', False):
#             raise ValueError("Account is locked due to too many failed attempts")

#         # Verify password
#         if not self.crypto.verify_password(password, user['password_hash']):
#             # Increment failed attempts
#             self.users_collection.update_one(
#                 {'user_id': user['user_id']},
#                 {
#                     '$inc': {'failed_login_attempts': 1},
#                     '$set': {
#                         'account_locked': user.get('failed_login_attempts', 0) + 1 >= 5
#                     }
#                 }
#             )
#             raise ValueError("Invalid credentials")

#         # Reset failed attempts on successful login
#         self.users_collection.update_one(
#             {'user_id': user['user_id']},
#             {
#                 '$set': {
#                     'failed_login_attempts': 0,
#                     'last_login': datetime.utcnow(),
#                     'account_locked': False
#                 }
#             }
#         )

#         # Create JWT tokens
#         access_token = create_access_token(
#             identity=user['user_id'],
#             additional_claims={'username': user['username']}
#         )
#         refresh_token = create_refresh_token(identity=user['user_id'])

#         return {
#             'access_token': access_token,
#             'refresh_token': refresh_token,
#             'user_id': user['user_id'],
#             'username': user['username'],
#             'public_key': user['public_key'],
#             'face_enabled': user.get('face_encoding') is not None,
#             'expires_in': 3600  # 1 hour
#         }

#     def verify_face_authentication(self, user_id: str, face_image: bytes) -> bool:
#         """Verify user identity using face recognition."""
#         user = self.users_collection.find_one({'user_id': user_id})
#         if not user or not user.get('face_encoding'):
#             return False

#         try:
#             new_face_encoding = self._process_face_image(face_image)
#             if new_face_encoding is None:
#                 return False

#             stored_encoding = user['face_encoding']
#             matches = face_recognition.compare_faces(
#                 [stored_encoding], 
#                 new_face_encoding, 
#                 tolerance=0.6
#             )

#             return matches[0] if matches else False

#         except Exception as e:
#             print(f"Face verification error: {e}")
#             return False

#     def setup_face_authentication(self, user_id: str, face_image: bytes) -> bool:
#         """Set up face authentication for a user."""
#         try:
#             face_encoding = self._process_face_image(face_image)
#             if face_encoding is None:
#                 return False

#             result = self.users_collection.update_one(
#                 {'user_id': user_id},
#                 {'$set': {'face_encoding': face_encoding}}
#             )

#             return result.modified_count > 0

#         except Exception as e:
#             print(f"Face setup error: {e}")
#             return False

#     def get_user_info(self, user_id: str) -> Optional[Dict[str, any]]:
#         """Get user information (excluding sensitive data)."""
#         user = self.users_collection.find_one({'user_id': user_id})
#         if not user:
#             return None

#         return {
#             'user_id': user['user_id'],
#             'username': user['username'],
#             'email': user['email'],
#             'public_key': user['public_key'],
#             'is_active': user['is_active'],
#             'created_at': user['created_at'],
#             'last_login': user.get('last_login'),
#             'face_enabled': user.get('face_encoding') is not None
#         }

#     def _process_face_image(self, image_data: bytes) -> Optional[list]:
#         """Process face image and extract face encoding."""
#         try:
#             # Load image from bytes
#             image = face_recognition.load_image_file(BytesIO(image_data))

#             # Find face encodings
#             face_encodings = face_recognition.face_encodings(image)

#             if len(face_encodings) == 0:
#                 return None
#             elif len(face_encodings) > 1:
#                 raise ValueError("Multiple faces detected. Please provide image with single face.")

#             return face_encodings[0].tolist()

#         except Exception as e:
#             print(f"Face processing error: {e}")
#             return None

# class MockCollection:
#     """Mock database collection for development without database."""
#     def __init__(self):
#         self.data = []

#     def find_one(self, query):
#         return None

#     def insert_one(self, document):
#         self.data.append(document)
#         return type('Result', (), {'inserted_id': 'mock_id'})()

#     def update_one(self, query, update):
#         return type('Result', (), {'modified_count': 1})()
