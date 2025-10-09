"""
SecureSession Configuration
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

    # Database settings
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/securesession')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'

    # File upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

    # Encryption settings
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    AES_KEY_SIZE = 32  # 256 bits
    RSA_KEY_SIZE = 2048

    # Session settings
    DEFAULT_SESSION_DURATION = 1  # hours
    MAX_SESSION_DURATION = 24     # hours

    # # Face recognition settings
    # FACE_RECOGNITION_TOLERANCE = 0.6
    # FACE_RECOGNITION_MODEL = 'hog'

    # Security settings
    BCRYPT_LOG_ROUNDS = 12
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 3600  # 1 hour

    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
