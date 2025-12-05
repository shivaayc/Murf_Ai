#!/usr/bin/env python3
"""
Setup script for MediVoice AI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print("✅ Python version check passed")

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "static/audio",
        "templates",
        "utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def create_environment_file():
    """Create .env file if it doesn't exist"""
    if not Path(".env").exists():
        env_content = """MURF_API_KEY=ap2_deeeb12f-ae13-43fe-80c1-009f39a81f82
DEEPGRAM_API_KEY=89bad04baa092952bfab9f11958aa784e57439a7
# OPENAI_API_KEY=your-openai-api-key-here  # Optional
# GROQ_API_KEY=your-groq-api-key-here      # Optional (free from console.groq.com)
PORT=8000
DEBUG=True
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print("✓ Created .env file")
    else:
        print("✓ .env file already exists")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Please install manually: pip install -r requirements.txt")

def check_csv_files():
    """Check if CSV files exist, create sample if not"""
    data_dir = Path("data")
    
    # Check medicines.csv
    med_file = data_dir / "medicines.csv"
    if not med_file.exists():
        print("⚠ medicines.csv not found. Creating sample data...")
        # Copy from your provided data or create minimal sample
        sample_csv = """name,generic_name,class,uses,dosage_adults,dosage_children,side_effects,contraindications,interactions,pregnancy,storage,brand_names,mechanism,onset,duration
Paracetamol,Acetaminophen,Analgesic/Antipyretic,Fever;Mild to moderate pain,500-1000mg every 4-6 hours max 4000mg/day,10-15mg/kg every 4-6 hours,Nausea;Rash;Liver damage (overdose),Severe liver disease,Alcohol;Warfarin,Category B - generally safe,Room temperature away from moisture,Crocin;Calpol,Inhibits prostaglandin synthesis,30 minutes,4-6 hours
Ibuprofen,Ibuprofen,NSAID,Pain;Inflammation;Fever;Arthritis,200-400mg every 4-6 hours max 1200mg/day,5-10mg/kg every 6-8 hours,Stomach pain;Nausea;Dizziness;Increased bleeding risk,Peptic ulcer;Kidney disease;Pregnancy (3rd trimester),Aspirin;Alcohol;Blood thinners,Avoid in 3rd trimester,Room temperature,Brufen;Advil,Inhibits COX enzymes;Reduces prostaglandins,30-60 minutes,4-6 hours"""
        
        med_file.write_text(sample_csv)
        print("✓ Created sample medicines.csv")
    
    # Check interactions.csv
    int_file = data_dir / "interactions.csv"
    if not int_file.exists():
        print("⚠ interactions.csv not found. Creating sample data...")
        sample_int = """medicine1,medicine2,severity,effect,recommendation,mechanism
Paracetamol,Alcohol,High,Increased risk of liver damage,Avoid or limit alcohol consumption,Induces CYP2E1 leading to toxic metabolite
Ibuprofen,Alcohol,High,Increased risk of stomach bleeding,Avoid alcohol while taking ibuprofen,Synergistic GI irritation"""
        
        int_file.write_text(sample_int)
        print("✓ Created sample interactions.csv")

def main():
    """Main setup function"""
    print("=" * 60)
    print("🎗️ MediVoice AI - Setup Script")
    print("=" * 60)
    
    # Run setup steps
    check_python_version()
    create_directories()
    create_environment_file()
    check_csv_files()
    
    print("\n📦 Installing dependencies...")
    install_dependencies()
    
    print("\n" + "=" * 60)
    print("✅ Setup completed successfully!")
    print("\nTo run MediVoice AI:")
    print("1. Edit .env file with your API keys")
    print("2. Add more medicines to data/medicines.csv")
    print("3. Run: python app.py")
    print("4. Open: http://localhost:8000")
    print("\nFor hackathon submission:")
    print("• Record a demo video")
    print("• Create GitHub repository")
    print("• Post on LinkedIn with @Murf AI tag")
    print("=" * 60)

if __name__ == "__main__":
    main()