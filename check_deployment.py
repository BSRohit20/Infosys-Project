#!/usr/bin/env python3
"""
ML-Optimized deployment verification script
Checks if the environment is ready for ML deployment
"""

import sys
import subprocess
import importlib

def check_package(package_name, import_name=None):
    """Check if a package is installed and can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} - OK")
        return True
    except ImportError:
        print(f"❌ {package_name} - MISSING")
        return False

def main():
    print("🔍 Checking ML Deployment Readiness...")
    print("=" * 50)
    
    # Core ML packages
    packages = [
        ("FastAPI", "fastapi"),
        ("Uvicorn", "uvicorn"),
        ("Transformers", "transformers"),
        ("PyTorch", "torch"),
        ("NumPy", "numpy"),
        ("Scikit-learn", "sklearn"),
        ("Pandas", "pandas"),
        ("Requests", "requests"),
        ("Python-JOSE", "jose"),
        ("Passlib", "passlib"),
    ]
    
    all_good = True
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_good = False
    
    print("=" * 50)
    
    if all_good:
        print("🎉 All packages ready for deployment!")
        print("\n🚀 Ready to deploy to:")
        print("   • Render.com (Recommended)")
        print("   • Railway.app")
        print("   • Hugging Face Spaces")
        return 0
    else:
        print("⚠️  Some packages are missing. Run:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
