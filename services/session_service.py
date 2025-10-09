# """
# Session Management Service for SecureSession
# Handles secure session creation, management, and automatic cleanup
# """
# import uuid
# import asyncio
# import json
# import base64
# from datetime import datetime, timedelta
# from typing import Dict, List, Optional, Any

# class SessionService:
#     """Session management service for SecureSession."""

#     def __init__(self, db, redis_client, crypto_service):
#         self.db = db
#         self.redis = redis_client
#         self.crypto = crypto_service

#         if self.db:
#             self.sessions_collection = db.secure_sessions
#             self.messages_collection = db.session_messages
#             self.files_collection = db.session_files
#         else:
#             # Mock collections for development
#             self.sessions_collection = MockSessionCollection()
#             self.messages_collection = MockSessionCollection()
#             self.files_collection = MockSessionCollection()

#         self.active_sessions = {}  # In-memory cache for active session keys

#     async def create_session(self, creator_id: str, recipient_email: str, 
#                            duration_hours: int = 1, attached_file: Dict = None) -> Dict[str, Any]:
#         """Create a new secure session between two users."""

#         # Generate unique session ID
#         session_id = str(uuid.uuid4())

#         # Generate session encryption key
#         session_key = self.crypto.generate_session_key()
#         session_key_b64 = base64.b64encode(session_key).decode('utf-8')

#         # Calculate expiration time
#         expires_at = datetime.utcnow() + timedelta(hours=duration_hours)

#         # Create session document
#         session_data = {
#             'session_id': session_id,
#             'creator_id': creator_id,
#             'recipient_email': recipient_email,
#             'status': 'pending',
#             'session_key': session_key_b64,
#             'created_at': datetime.utcnow(),
#             'expires_at': expires_at,
#             'duration_hours': duration_hours,
#             'messages': [],
#             'files': [],
#             'invitation_sent': False,
#             'invitation_accepted': False,
#             'destroyed_at': None
#         }

#         # Save session to database
#         self.sessions_collection.insert_one(session_data)

#         # Cache session key in Redis for quick access (if available)
#         if self.redis:
#             try:
#                 self.redis.setex(
#                     f"session:{session_id}:key",
#                     duration_hours * 3600,
#                     session_key_b64
#                 )
#             except:
#                 pass  # Continue without Redis caching

#         # Store in active sessions cache
#         self.active_sessions[session_id] = {
#             'key': session_key,
#             'creator_id': creator_id,
#             'recipient_email': recipient_email,
#             'expires_at': expires_at
#         }

#         return {
#             'session_id': session_id,
#             'status': 'pending',
#             'recipient_email': recipient_email,
#             'expires_at': expires_at.isoformat(),
#             'duration_hours': duration_hours,
#             'has_attached_file': attached_file is not None
#         }

#     async def send_message(self, session_id: str, sender_id: str, 
#                           message: str, message_type: str = 'text') -> Dict[str, Any]:
#         """Send an encrypted message in a session."""

#         # Get session key
#         session_key = await self._get_session_key(session_id)
#         if not session_key:
#             raise ValueError("Session key not found")

#         # Encrypt message
#         encrypted_data = self.crypto.encrypt_aes_256_gcm(
#             message.encode('utf-8'), session_key
#         )

#         # Create message document
#         message_data = {
#             'message_id': str(uuid.uuid4()),
#             'session_id': session_id,
#             'sender_id': sender_id,
#             'message_type': message_type,
#             'encrypted_content': base64.b64encode(encrypted_data['ciphertext']).decode('utf-8'),
#             'iv': base64.b64encode(encrypted_data['iv']).decode('utf-8'),
#             'tag': base64.b64encode(encrypted_data['tag']).decode('utf-8'),
#             'sent_at': datetime.utcnow(),
#             'is_deleted': False
#         }

#         # Save message
#         self.messages_collection.insert_one(message_data)

#         return {
#             'message_id': message_data['message_id'],
#             'sent_at': message_data['sent_at'].isoformat(),
#             'encrypted': True
#         }

#     async def get_session_messages(self, session_id: str, user_id: str, 
#                                   limit: int = 50) -> List[Dict[str, Any]]:
#         """Get decrypted messages for a session."""

#         # Get session key
#         session_key = await self._get_session_key(session_id)
#         if not session_key:
#             raise ValueError("Session key not found")

#         # Get messages from database (mock implementation)
#         messages = []

#         return messages

#     async def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
#         """Get all sessions for a user."""
#         # Mock implementation - return active sessions from cache
#         user_sessions = []

#         for session_id, session_info in self.active_sessions.items():
#             if session_info.get('creator_id') == user_id:
#                 user_sessions.append({
#                     'session_id': session_id,
#                     'status': 'active',
#                     'is_creator': True,
#                     'recipient_email': session_info.get('recipient_email'),
#                     'expires_at': session_info.get('expires_at').isoformat(),
#                     'created_at': datetime.utcnow().isoformat()
#                 })

#         return user_sessions

#     async def _get_session_key(self, session_id: str) -> Optional[bytes]:
#         """Get session encryption key."""
#         # Try cache first
#         if session_id in self.active_sessions:
#             return self.active_sessions[session_id]['key']

#         # Try Redis cache
#         if self.redis:
#             try:
#                 cached_key = self.redis.get(f"session:{session_id}:key")
#                 if cached_key:
#                     return base64.b64decode(cached_key)
#             except:
#                 pass

#         return None

# class MockSessionCollection:
#     """Mock session collection for development."""
#     def __init__(self):
#         self.data = []

#     def find_one(self, query):
#         return None

#     def insert_one(self, document):
#         self.data.append(document)
#         return type('Result', (), {'inserted_id': 'mock_id'})()

#     def update_one(self, query, update):
#         return type('Result', (), {'modified_count': 1})()

#     def find(self, query):
#         return []
