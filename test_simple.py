#!/usr/bin/env python3
"""
Test script for MediVoice AI (Simple Version)
"""

import os
import sys

def check_dependencies():
    """Check if all dependencies are installed"""
    required = [
        'fastapi',
        'uvicorn', 
        'requests',
        'deepgram',
        'aiofiles',
        'apscheduler'
    ]
    
    print("🔍 Checking dependencies...")
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing: {', '.join(missing)}")
        print("Run: pip install " + " ".join(missing))
        return False
    return True

def check_env():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("Create .env with MURF_API_KEY and DEEPGRAM_API_KEY")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'MURF_API_KEY' not in content:
            print("❌ MURF_API_KEY missing in .env")
            return False
        if 'DEEPGRAM_API_KEY' not in content:
            print("❌ DEEPGRAM_API_KEY missing in .env")
            return False
    
    print("✅ .env file OK")
    return True

def main():
    print("=" * 50)
    print("MediVoice AI - System Check")
    print("=" * 50)
    
    # Check Python version
    print(f"Python: {sys.version.split()[0]}")
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check .env
    if not check_env():
        return
    
    print("\n" + "=" * 50)
    print("✅ All checks passed!")
    print("\nTo run:")
    print("1. python app.py")
    print("2. Open: http://localhost:8000")
    print("=" * 50)

if __name__ == "__main__":
    main()