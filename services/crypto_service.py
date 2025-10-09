# """
# Cryptography Service for SecureSession
# Handles all encryption, decryption, and key management operations
# """
# import os
# import base64
# import secrets
# from datetime import datetime
# from typing import Dict, Optional, Tuple, Any

# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# from cryptography.hazmat.primitives import hashes, serialization
# from cryptography.hazmat.primitives.asymmetric import rsa, ec
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.backends import default_backend
# from cryptography.fernet import Fernet

# class CryptoService:
#     """
#     Comprehensive cryptography service for SecureSession.
#     Implements AES-256, RSA, and ECC encryption algorithms.
#     """

#     def __init__(self):
#         self.backend = default_backend()

#     def generate_rsa_keypair(self, key_size: int = 2048) -> Dict[str, Any]:
#         """Generate RSA public/private key pair."""
#         private_key = rsa.generate_private_key(
#             public_exponent=65537,
#             key_size=key_size,
#             backend=self.backend
#         )
#         public_key = private_key.public_key()

#         private_pem = private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption()
#         )

#         public_pem = public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         )

#         return {
#             'private_key': private_key,
#             'public_key': public_key,
#             'private_pem': private_pem.decode('utf-8'),
#             'public_pem': public_pem.decode('utf-8'),
#             'fingerprint': self._generate_key_fingerprint(public_pem)
#         }

#     def generate_session_key(self) -> bytes:
#         """Generate a cryptographically secure AES-256 session key."""
#         return os.urandom(32)  # 256 bits

#     def encrypt_aes_256_gcm(self, data: bytes, key: bytes) -> Dict[str, bytes]:
#         """Encrypt data using AES-256-GCM."""
#         if len(key) != 32:
#             raise ValueError("AES-256 key must be 32 bytes")

#         iv = os.urandom(12)  # 96-bit IV for GCM
#         cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=self.backend)
#         encryptor = cipher.encryptor()

#         ciphertext = encryptor.update(data) + encryptor.finalize()

#         return {
#             'ciphertext': ciphertext,
#             'iv': iv,
#             'tag': encryptor.tag,
#             'algorithm': 'AES-256-GCM'
#         }

#     def decrypt_aes_256_gcm(self, ciphertext: bytes, key: bytes, iv: bytes, tag: bytes) -> bytes:
#         """Decrypt data using AES-256-GCM."""
#         if len(key) != 32:
#             raise ValueError("AES-256 key must be 32 bytes")

#         cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=self.backend)
#         decryptor = cipher.decryptor()

#         plaintext = decryptor.update(ciphertext) + decryptor.finalize()
#         return plaintext

#     def encrypt_file(self, file_data: bytes, session_key: bytes) -> Dict[str, Any]:
#         """Encrypt file data for secure transfer."""
#         encrypted_data = self.encrypt_aes_256_gcm(file_data, session_key)

#         return {
#             'encrypted_data': encrypted_data,
#             'original_size': len(file_data),
#             'encrypted_size': len(encrypted_data['ciphertext']),
#             'timestamp': datetime.utcnow().isoformat()
#         }

#     def decrypt_file(self, encrypted_info: Dict[str, Any], session_key: bytes) -> bytes:
#         """Decrypt file data."""
#         encrypted_data = encrypted_info['encrypted_data']
#         return self.decrypt_aes_256_gcm(
#             encrypted_data['ciphertext'],
#             session_key,
#             encrypted_data['iv'],
#             encrypted_data['tag']
#         )

#     def hash_password(self, password: str) -> str:
#         """Hash password using Argon2."""
#         from argon2 import PasswordHasher
#         ph = PasswordHasher()
#         return ph.hash(password)

#     def verify_password(self, password: str, hashed: str) -> bool:
#         """Verify password against hash."""
#         from argon2 import PasswordHasher
#         from argon2.exceptions import VerifyMismatchError

#         ph = PasswordHasher()
#         try:
#             ph.verify(hashed, password)
#             return True
#         except VerifyMismatchError:
#             return False

#     def generate_secure_token(self, length: int = 32) -> str:
#         """Generate a cryptographically secure random token."""
#         return secrets.token_urlsafe(length)

#     def _generate_key_fingerprint(self, public_key_pem: bytes) -> str:
#         """Generate fingerprint for a public key."""
#         digest = hashes.Hash(hashes.SHA256(), backend=self.backend)
#         digest.update(public_key_pem)
#         fingerprint = digest.finalize()
#         return base64.b64encode(fingerprint).decode('utf-8')

#     def secure_compare(self, a: str, b: str) -> bool:
#         """Constant-time string comparison to prevent timing attacks."""
#         return secrets.compare_digest(a.encode('utf-8'), b.encode('utf-8'))
