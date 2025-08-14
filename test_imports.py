#!/usr/bin/env python3
"""
Test script to check if all dependencies are installed
"""

def test_imports():
    try:
        print("Testing imports...")
        
        # Basic Flask
        from flask import Flask
        print("✅ Flask imported successfully")
        
        # Flask extensions
        from flask_sqlalchemy import SQLAlchemy
        print("✅ Flask-SQLAlchemy imported successfully")
        
        from flask_login import LoginManager
        print("✅ Flask-Login imported successfully")
        
        from flask_wtf.csrf import CSRFProtect
        print("✅ Flask-WTF imported successfully")
        
        # WTForms with email validation
        from wtforms.validators import Email
        print("✅ WTForms Email validator imported successfully")
        
        # System utilities
        import psutil
        print("✅ psutil imported successfully")
        
        import requests
        print("✅ requests imported successfully")
        
        # Environment
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
        
        # Test app creation
        from app import create_app
        print("✅ App module imported successfully")
        
        print("\n🎉 All imports successful! Ready to start the application.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

if __name__ == "__main__":
    if test_imports():
        print("\n🚀 You can now run: python app.py")
    else:
        print("\n⚠️  Please install missing dependencies with: pip install -r requirements.txt")
