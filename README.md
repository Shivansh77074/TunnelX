# SecureSession Backend

End-to-end encrypted file transfer system backend built with Flask.

## Features

- **AES-256-GCM Encryption**: Symmetric encryption for session data
- **RSA/ECC Key Exchange**: Asymmetric encryption for secure key exchange
- **Face Recognition**: Biometric authentication using face recognition
- **JWT Authentication**: Secure token-based authentication
- **Session Management**: Ephemeral sessions with automatic destruction
- **Real-time Messaging**: WebSocket support for real-time communication
- **File Upload**: Encrypted file transfer capabilities

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run the Application**
   ```bash
   python run.py
   ```

4. **Access the API**
   - Base URL: http://localhost:5000
   - Health Check: http://localhost:5000/api/health

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/face-verify` - Face verification
- `POST /api/auth/setup-face` - Setup face authentication
- `GET /api/auth/profile` - Get user profile

### Sessions
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - Get user sessions
- `POST /api/sessions/{id}/messages` - Send message
- `GET /api/sessions/{id}/messages` - Get messages

### Files
- `POST /api/files/upload` - Upload encrypted file
- `GET /api/files/{id}/download` - Download file
- `DELETE /api/files/{id}` - Delete file

## Project Structure

```
├── run.py                    # Application entry point
├── app.py                    # Flask application factory
├── config.py                 # Configuration settings
├── services/                 # Business logic services
│   ├── crypto_service.py     # Cryptography operations
│   ├── auth_service.py       # Authentication logic
│   ├── session_service.py    # Session management
│   └── face_service.py       # Face recognition
├── routes/                   # API routes
│   ├── auth_routes.py        # Authentication endpoints
│   ├── session_routes.py     # Session endpoints
│   └── file_routes.py        # File endpoints
├── requirements.txt          # Python dependencies
└── .env                      # Environment configuration
```

## Security Features

- **End-to-End Encryption**: All data encrypted before transmission
- **Zero-Knowledge Architecture**: Server cannot decrypt user data
- **Perfect Forward Secrecy**: Unique session keys per session
- **Secure Key Management**: Cryptographically secure key generation
- **Password Hashing**: Argon2 password hashing
- **Rate Limiting**: Protection against brute force attacks
- **Input Validation**: Comprehensive input sanitization

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black .
flake8 .
```

### Docker Development
```bash
docker build -t securesession-backend .
docker run -p 5000:5000 securesession-backend
```

## Production Deployment

1. **Set production environment variables**
2. **Use a production WSGI server** (gunicorn included)
3. **Set up MongoDB and Redis** with proper authentication
4. **Configure SSL/TLS** for HTTPS
5. **Set up monitoring and logging**

## License

MIT License - see LICENSE file for details.
