#!/usr/bin/env python3
"""
SecureSession Backend - Main Application Entry Point
"""
import os
from app import create_app

if __name__ == '__main__':
    # Create Flask application
    app = create_app()
    # app,socketio = create_app()

    # Run the application
    # socketio.run(
    #     app,
    #     debug=True,
    #     host='0.0.0.0',
    #     port=int(os.environ.get('PORT', 5000))
    # )

#<-------------------------------------------------------------------------------------------------------------------------------------------------------

#!/usr/bin/env python3
"""
SecureSession Backend - Main Application Entry Point (Basic API Test)
"""
import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env
load_dotenv()

if __name__ == '__main__':
    # Create Flask application
    app = create_app()  # socketio will not be used now
    # app,socketio = create_app()

    # Get port from .env (default 5000 if not set)
    port = int(os.environ.get('PORT', 5000))

    # Run Flask app only (without SocketIO)
    print(f"Starting basic API server on port {port}...")
    app.run(
        debug=True,   # enables auto-reload and debug messages
        host='0.0.0.0',
        port=port
    )

    # If you want to enable SocketIO later, uncomment this:
    # socketio.run(app, debug=True, host='0.0.0.0', port=port)
