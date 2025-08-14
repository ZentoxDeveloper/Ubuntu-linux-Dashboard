#!/usr/bin/env python3
"""
Ubuntu Server Dashboard - Startup Script met Error Handling
"""
import os
import sys
from dotenv import load_dotenv

def main():
    print("🚀 Ubuntu Server Dashboard - Starting...")
    print("=" * 50)
    
    # Load environment variables
    try:
        load_dotenv()
        print("✅ Environment variables loaded")
    except Exception as e:
        print(f"⚠️  Warning: Could not load .env file: {e}")
    
    # Test imports
    try:
        print("📦 Testing imports...")
        from app import create_app
        print("✅ App imports successful")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("💡 Try: pip install -r requirements.txt")
        return False
    
    # Create app
    try:
        app = create_app(os.environ.get('FLASK_ENV', 'development'))
        print("✅ Flask app created successfully")
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False
    
    # Start server
    try:
        host = os.environ.get('FLASK_HOST', '0.0.0.0')
        port = int(os.environ.get('FLASK_PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
        
        print(f"🌐 Starting server on http://{host}:{port}")
        print("👤 Default login: admin / admin123")
        print("⚠️  Change default password after first login!")
        print("=" * 50)
        
        app.run(host=host, port=port, debug=debug)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return False

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)
